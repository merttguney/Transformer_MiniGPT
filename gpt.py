from __future__ import annotations
import numpy as np
from typing import Dict, List, Optional, Tuple
from embedding import positional_encoding, embedding_forward, embedding_backward
from transformer_block import TransformerBlock, he_init, layer_norm_forward, layer_norm_backward
from attention import causal_mask, dropout_forward, dropout_backward


class GPT:
    def __init__(
        self,
        vocab_size: int,
        d_model: int = 128,
        n_heads: int = 4,
        n_layers: int = 3,
        d_ff: int = 512,
        context_length: int = 128,
        dropout: float = 0.1,
    ):
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.context_length = context_length
        self.dropout = dropout

        # Token embedding
        self.token_embedding = (
            np.random.randn(vocab_size, d_model).astype(np.float32) * np.sqrt(2.0 / vocab_size)
        )
        # Sinusoidal positional encoding (sabit, eğitilmiyor)
        self.pos_encoding = positional_encoding(context_length, d_model)

        # Transformer blokları
        self.blocks = [TransformerBlock(d_model, n_heads, d_ff, dropout) for _ in range(n_layers)]

        # Final LayerNorm (Pre-LN mimarisinde gerekli)
        self.ln_final_gamma = np.ones((d_model,), np.float32)
        self.ln_final_beta = np.zeros((d_model,), np.float32)

        # Vocab projection
        self.W_vocab = he_init(d_model, vocab_size)
        self.b_vocab = np.zeros((vocab_size,), np.float32)

        # Gradientler
        self.grads: Dict[str, np.ndarray] = {
            "token_embedding": np.zeros_like(self.token_embedding),
            "ln_final_gamma": np.zeros_like(self.ln_final_gamma),
            "ln_final_beta": np.zeros_like(self.ln_final_beta),
            "W_vocab": np.zeros_like(self.W_vocab),
            "b_vocab": np.zeros_like(self.b_vocab),
        }

    # ── Forward ──
    def forward(
        self,
        x_ids: np.ndarray,
        return_cache: bool = False,
        return_attn: bool = False,
        training: bool = False,
    ):
        m = causal_mask(x_ids.shape[1])
        h, ec = embedding_forward(x_ids, self.token_embedding, self.pos_encoding)

        # Embedding dropout
        h, emb_drop = dropout_forward(h, self.dropout, training)

        bcs, atts = [], []
        for b in self.blocks:
            h, a, c = b.forward(h, m, training)
            bcs.append(c)
            atts.append(a)

        # Final LayerNorm
        h, ln_fc = layer_norm_forward(h, self.ln_final_gamma, self.ln_final_beta)

        logits = h @ self.W_vocab + self.b_vocab

        if not return_cache and not return_attn:
            return logits
        out = [logits]
        if return_cache:
            out.append({"h": h, "ec": ec, "bcs": bcs, "ln_fc": ln_fc, "emb_drop": emb_drop})
        if return_attn:
            out.append(atts)
        return tuple(out)

    # ── Backward ──
    def backward(self, dlogits: np.ndarray, c: Dict):
        for k in self.grads:
            self.grads[k].fill(0.0)

        h = c["h"]
        self.grads["W_vocab"] += h.reshape(-1, h.shape[-1]).T @ dlogits.reshape(-1, dlogits.shape[-1])
        self.grads["b_vocab"] += np.sum(dlogits, axis=(0, 1))
        dh = dlogits @ self.W_vocab.T

        # Final LayerNorm backward
        dh, g_fg, b_fg = layer_norm_backward(dh, c["ln_fc"])
        self.grads["ln_final_gamma"] += g_fg
        self.grads["ln_final_beta"] += b_fg

        # Transformer blokları backward
        for i in reversed(range(len(self.blocks))):
            dh = self.blocks[i].backward(dh, c["bcs"][i])

        # Embedding dropout backward
        dh = dropout_backward(dh, c["emb_drop"])

        self.grads["token_embedding"] += embedding_backward(dh, c["ec"], self.token_embedding)

    # ── Parametreler ──
    def parameters_and_grads(self) -> List[Tuple[str, np.ndarray, np.ndarray]]:
        out = [
            ("token_embedding", self.token_embedding, self.grads["token_embedding"]),
            ("ln_final_gamma", self.ln_final_gamma, self.grads["ln_final_gamma"]),
            ("ln_final_beta", self.ln_final_beta, self.grads["ln_final_beta"]),
            ("W_vocab", self.W_vocab, self.grads["W_vocab"]),
            ("b_vocab", self.b_vocab, self.grads["b_vocab"]),
        ]
        for i, b in enumerate(self.blocks):
            for k in b.params:
                out.append((f"blocks.{i}.{k}", b.params[k], b.grads[k]))
        return out

    def num_parameters(self) -> int:
        return sum(p.size for _, p, _ in self.parameters_and_grads())

    # ── State Dict ──
    def state_dict(self) -> Dict[str, np.ndarray]:
        sd: Dict[str, np.ndarray] = {
            "token_embedding": self.token_embedding,
            "ln_final_gamma": self.ln_final_gamma,
            "ln_final_beta": self.ln_final_beta,
            "W_vocab": self.W_vocab,
            "b_vocab": self.b_vocab,
        }
        for i, b in enumerate(self.blocks):
            for k, v in b.params.items():
                sd[f"blocks.{i}.{k}"] = v
        return sd

    def load_state_dict(self, sd: Dict[str, np.ndarray]):
        self.token_embedding[:] = sd["token_embedding"]
        self.ln_final_gamma[:] = sd["ln_final_gamma"]
        self.ln_final_beta[:] = sd["ln_final_beta"]
        self.W_vocab[:] = sd["W_vocab"]
        self.b_vocab[:] = sd["b_vocab"]
        for i, b in enumerate(self.blocks):
            for k in b.params:
                b.params[k][:] = sd[f"blocks.{i}.{k}"]

    # ── Generate (Top-K + Top-P + Repetition Penalty) ──
    def generate(
        self,
        prompt_ids: List[int],
        max_tokens: int = 80,
        temperature: float = 0.55,
        top_k: int = 20,
        top_p: Optional[float] = 0.9,
        repetition_penalty: float = 0.15,
        rep_window: int = 48,
        eos_id: Optional[int] = None,
    ) -> List[int]:
        ids = list(prompt_ids)
        for _ in range(max_tokens):
            x = np.array([ids[-self.context_length:]], dtype=np.int32)
            logits = self.forward(x, training=False)
            z = logits[0, -1].astype(np.float64)

            # Temperature
            z = z / max(temperature, 1e-6)

            # Repetition penalty
            if repetition_penalty > 0:
                recent = ids[-rep_window:] if len(ids) > rep_window else ids
                if recent:
                    z[np.array(recent, dtype=np.int32)] -= repetition_penalty

            # Top-K
            if top_k is not None and top_k > 0:
                k = min(top_k, z.shape[0])
                idx = np.argpartition(z, -k)[-k:]
                masked = np.full_like(z, -1e10)
                masked[idx] = z[idx]
                z = masked

            p = np.exp(z - np.max(z))
            p /= np.sum(p)

            # Top-P (Nucleus)
            if top_p is not None and 0 < top_p < 1.0:
                sorted_idx = np.argsort(-p)
                cumsum = np.cumsum(p[sorted_idx])
                cutoff = np.searchsorted(cumsum, top_p) + 1
                keep = sorted_idx[:cutoff]
                filtered = np.zeros_like(p)
                filtered[keep] = p[keep]
                filtered /= np.sum(filtered)
                p = filtered

            next_id = int(np.random.choice(len(p), p=p))

            # EOS durdurma
            if eos_id is not None and next_id == eos_id:
                break

            ids.append(next_id)
        return ids

    # ── Attention Görselleştirme ──
    def attention_matrix(self, text_ids: List[int]) -> np.ndarray:
        x = np.array([text_ids[-self.context_length:]], dtype=np.int32)
        _, _, atts = self.forward(x, return_cache=True, return_attn=True, training=False)
        return np.mean(atts[-1][0], axis=0)
