from __future__ import annotations
import os, json, time
import numpy as np
from typing import Dict, List, Tuple

from config import GPTConfig
from data.corpus import build_corpus
from data.tokenizer import CharTokenizer
from model.gpt import GPT


# ────────────────────────────────────────
# Veri Hazırlama
# ────────────────────────────────────────

def make_batches(ids: List[int], context_length: int, batch_size: int) -> Tuple[np.ndarray, np.ndarray]:
    max_start = len(ids) - context_length - 1
    s = np.random.randint(0, max_start, size=batch_size)
    x = np.array([ids[i : i + context_length] for i in s], np.int32)
    y = np.array([ids[i + 1 : i + context_length + 1] for i in s], np.int32)
    return x, y


# ────────────────────────────────────────
# Loss
# ────────────────────────────────────────

def cross_entropy_loss_and_grad(logits: np.ndarray, targets: np.ndarray):
    b, t, v = logits.shape
    fl = logits.reshape(-1, v)
    ft = targets.reshape(-1)
    z = fl - np.max(fl, axis=1, keepdims=True)
    e = np.exp(z)
    p = e / np.sum(e, axis=1, keepdims=True)
    n = fl.shape[0]
    loss = -np.log(p[np.arange(n), ft] + 1e-12).mean()
    d = p.copy()
    d[np.arange(n), ft] -= 1.0
    d /= n
    return float(loss), d.reshape(b, t, v)


# ────────────────────────────────────────
# AdamW Optimizer
# ────────────────────────────────────────

def adamw_step(
    params,
    state: Dict,
    t: int,
    lr: float,
    weight_decay: float = 0.01,
    b1: float = 0.9,
    b2: float = 0.999,
    eps: float = 1e-8,
):
    # weight_decay uygulanMAYACAK parametreler (bias, LayerNorm)
    no_decay = {"b_Q", "b_K", "b_V", "b_O", "b1", "b2", "b_vocab",
                "ln1_gamma", "ln1_beta", "ln2_gamma", "ln2_beta",
                "ln_final_gamma", "ln_final_beta"}

    for name, p, g in params:
        if name not in state:
            state[name] = {"m": np.zeros_like(p), "v": np.zeros_like(p)}
        m, v = state[name]["m"], state[name]["v"]
        m[:] = b1 * m + (1 - b1) * g
        v[:] = b2 * v + (1 - b2) * (g * g)
        mh = m / (1 - b1 ** t)
        vh = v / (1 - b2 ** t)

        # AdamW: weight decay ayrı uygulanır
        param_name = name.split(".")[-1]  # blocks.0.W_Q -> W_Q
        wd = 0.0 if param_name in no_decay else weight_decay
        p[:] = p * (1.0 - lr * wd) - lr * mh / (np.sqrt(vh) + eps)


# ────────────────────────────────────────
# Learning Rate Schedule
# ────────────────────────────────────────

def lr_schedule(step: int, warmup_steps: int, total_steps: int, max_lr: float, min_lr: float = 1e-5) -> float:
    if step < warmup_steps:
        return max_lr * step / max(1, warmup_steps)
    progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
    return min_lr + 0.5 * (max_lr - min_lr) * (1.0 + np.cos(np.pi * progress))


# ────────────────────────────────────────
# Gradient Clipping
# ────────────────────────────────────────

def clip_gradients(params, max_norm: float) -> float:
    total_norm_sq = 0.0
    for _, _, g in params:
        total_norm_sq += np.sum(g * g)
    total_norm = float(np.sqrt(total_norm_sq))
    if total_norm > max_norm:
        scale = max_norm / (total_norm + 1e-8)
        for _, _, g in params:
            g *= scale
    return total_norm


# ────────────────────────────────────────
# Ana Eğitim Fonksiyonu
# ────────────────────────────────────────

def train_model(cfg: GPTConfig | None = None):
    if cfg is None:
        cfg = GPTConfig()

    np.random.seed(cfg.seed)

    # Corpus
    corpus = build_corpus()
    tok = CharTokenizer.from_text(corpus)
    cfg.vocab_size = tok.vocab_size
    ids = tok.encode(corpus)
    print(f"[veri] Corpus: {len(corpus):,} karakter | Vocab: {tok.vocab_size} | Token: {len(ids):,}")

    # Train/Val split
    split = int(len(ids) * (1 - cfg.val_ratio))
    train_ids = ids[:split]
    val_ids = ids[split:]
    print(f"[veri] Train: {len(train_ids):,} | Val: {len(val_ids):,}")

    # Model
    model = GPT(
        cfg.vocab_size, cfg.d_model, cfg.n_heads, cfg.n_layers,
        cfg.d_ff, cfg.context_length, cfg.dropout,
    )
    print(f"[model] Parametreler: {model.num_parameters():,}")

    steps_per_epoch = max(1, len(train_ids) // (cfg.batch_size * cfg.context_length))
    total_steps = cfg.epochs * steps_per_epoch
    cfg.warmup_steps = min(cfg.warmup_steps, total_steps // 4)

    train_losses, val_losses = [], []
    opt_state: Dict = {}
    global_step = 0
    best_val = float("inf")
    t0 = time.time()

    for ep in range(1, cfg.epochs + 1):
        ep_losses = []
        for _ in range(steps_per_epoch):
            global_step += 1

            # LR schedule
            lr = lr_schedule(global_step, cfg.warmup_steps, total_steps, cfg.learning_rate)

            x, y = make_batches(train_ids, cfg.context_length, cfg.batch_size)
            logits, cache = model.forward(x, return_cache=True, training=True)
            loss, dlogits = cross_entropy_loss_and_grad(logits, y)
            model.backward(dlogits, cache)

            # Gradient clipping
            pag = model.parameters_and_grads()
            clip_gradients(pag, cfg.grad_clip)

            # AdamW step
            adamw_step(pag, opt_state, global_step, lr, cfg.weight_decay)
            ep_losses.append(loss)

        train_loss = float(np.mean(ep_losses))
        train_losses.append(train_loss)

        # Validation
        val_loss = _evaluate(model, val_ids, cfg.context_length, cfg.batch_size)
        val_losses.append(val_loss)

        perplexity = float(np.exp(min(val_loss, 20)))
        elapsed = time.time() - t0

        print(
            f"Epoch {ep:03d}/{cfg.epochs} | "
            f"train={train_loss:.4f} | val={val_loss:.4f} | "
            f"ppl={perplexity:.1f} | lr={lr:.2e} | "
            f"t={elapsed:.0f}s"
        )

        # Best model kaydet
        if val_loss < best_val:
            best_val = val_loss
            _save_checkpoint(model, tok, cfg, train_losses, val_losses)

    # Son model de kaydet
    _save_checkpoint(model, tok, cfg, train_losses, val_losses)
    return model, tok, train_losses, val_losses


def _evaluate(model: GPT, ids: List[int], context_length: int, batch_size: int) -> float:
    n_batches = max(1, len(ids) // (batch_size * context_length) // 2)
    losses = []
    for _ in range(n_batches):
        x, y = make_batches(ids, context_length, min(batch_size, 8))
        logits = model.forward(x, training=False)
        loss, _ = cross_entropy_loss_and_grad(logits, y)
        losses.append(loss)
    return float(np.mean(losses))


def _save_checkpoint(model, tok, cfg, train_losses, val_losses):
    os.makedirs("checkpoints", exist_ok=True)
    np.savez("checkpoints/mini_gpt.npz", **model.state_dict())

    with open("checkpoints/tokenizer.json", "w", encoding="utf-8") as f:
        json.dump({"stoi": tok.stoi}, f, ensure_ascii=False, indent=2)

    cfg.save("checkpoints/config.json")

    with open("checkpoints/train_info.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "d_model": cfg.d_model,
                "n_heads": cfg.n_heads,
                "n_layers": cfg.n_layers,
                "d_ff": cfg.d_ff,
                "context_length": cfg.context_length,
                "dropout": cfg.dropout,
                "batch_size": cfg.batch_size,
                "learning_rate": cfg.learning_rate,
                "weight_decay": cfg.weight_decay,
                "epochs": cfg.epochs,
                "final_loss": train_losses[-1],
                "best_val_loss": min(val_losses),
                "vocab_size": cfg.vocab_size,
                "num_parameters": model.num_parameters(),
                "train_losses": train_losses,
                "val_losses": val_losses,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
