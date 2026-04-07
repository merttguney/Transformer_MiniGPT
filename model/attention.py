from __future__ import annotations
import numpy as np
from typing import Dict, Optional, Tuple


# ────────────────────────────────────────
# Yardımcı fonksiyonlar
# ────────────────────────────────────────

def _softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Numerik stabil softmax."""
    x = x - np.max(x, axis=axis, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=axis, keepdims=True)


def causal_mask(t: int) -> np.ndarray:
    """Üst üçgensel nedensel maske."""
    m = np.triu(np.ones((t, t), dtype=np.float32), k=1)
    return m * -1e9


def dropout_forward(x: np.ndarray, p: float, training: bool) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """Inverted dropout forward — maske 1/(1-p) ölçeğini içerir."""
    if not training or p <= 0.0:
        return x, None
    mask = (np.random.rand(*x.shape) > p).astype(np.float32) / (1.0 - p)
    return x * mask, mask


def dropout_backward(dout: np.ndarray, mask: Optional[np.ndarray]) -> np.ndarray:
    """Dropout backward — mask zaten ölçek içeriyor."""
    if mask is None:
        return dout
    return dout * mask


# ────────────────────────────────────────
# Scaled Dot-Product Attention
# ────────────────────────────────────────

def scaled_dot_product_attention(
    q: np.ndarray,
    k: np.ndarray,
    v: np.ndarray,
    mask: Optional[np.ndarray],
    dropout_p: float = 0.0,
    training: bool = False,
):
    d_k = q.shape[-1]
    scores = (q @ np.swapaxes(k, -1, -2)) / np.sqrt(d_k)
    if mask is not None:
        scores = scores + mask[None, None, :, :]

    attn_raw = _softmax(scores, axis=-1)

    # Attention dropout
    attn, drop_mask = dropout_forward(attn_raw, dropout_p, training)

    out = attn @ v
    cache = {
        "q": q, "k": k, "v": v,
        "attn_raw": attn_raw, "attn": attn,
        "d_k": d_k, "drop_mask": drop_mask,
    }
    return out, attn_raw, cache


def scaled_dot_product_attention_backward(dout: np.ndarray, c: Dict):
    q, k, v = c["q"], c["k"], c["v"]
    attn_raw, attn = c["attn_raw"], c["attn"]
    d_k, drop_mask = c["d_k"], c["drop_mask"]

    d_attn = dout @ np.swapaxes(v, -1, -2)
    d_v = np.swapaxes(attn, -1, -2) @ dout

    # Dropout backward
    d_attn_raw = dropout_backward(d_attn, drop_mask)

    # Softmax backward
    tmp = np.sum(d_attn_raw * attn_raw, axis=-1, keepdims=True)
    d_scores = attn_raw * (d_attn_raw - tmp)

    s = 1.0 / np.sqrt(d_k)
    d_q = (d_scores @ k) * s
    d_km = (np.swapaxes(d_scores, -1, -2) @ q) * s
    return d_q, d_km, d_v


# ────────────────────────────────────────
# Multi-Head Attention
# ────────────────────────────────────────

def multi_head_attention_forward(
    x: np.ndarray,
    p: Dict[str, np.ndarray],
    n_heads: int,
    mask: Optional[np.ndarray],
    dropout_p: float = 0.0,
    training: bool = False,
):
    b, t, d = x.shape
    hd = d // n_heads

    q = x @ p["W_Q"] + p["b_Q"]
    k = x @ p["W_K"] + p["b_K"]
    v = x @ p["W_V"] + p["b_V"]

    qh = q.reshape(b, t, n_heads, hd).transpose(0, 2, 1, 3)
    kh = k.reshape(b, t, n_heads, hd).transpose(0, 2, 1, 3)
    vh = v.reshape(b, t, n_heads, hd).transpose(0, 2, 1, 3)

    oh, attn_weights, ac = scaled_dot_product_attention(
        qh, kh, vh, mask, dropout_p, training,
    )
    out = oh.transpose(0, 2, 1, 3).reshape(b, t, d)
    y = out @ p["W_O"] + p["b_O"]

    cache = {
        "x": x, "out": out,
        "q": q, "k": k, "v": v,
        "qh": qh, "kh": kh, "vh": vh,
        "ac": ac, "n_heads": n_heads,
    }
    return y, attn_weights, cache


def multi_head_attention_backward(dy: np.ndarray, c: Dict, p: Dict[str, np.ndarray]):
    x, out, n_heads, ac = c["x"], c["out"], c["n_heads"], c["ac"]
    grads = {k: np.zeros_like(v) for k, v in p.items()}
    b, t, d = x.shape
    hd = d // n_heads

    grads["W_O"] = out.reshape(-1, d).T @ dy.reshape(-1, d)
    grads["b_O"] = np.sum(dy, axis=(0, 1))
    d_out = dy @ p["W_O"].T
    d_oh = d_out.reshape(b, t, n_heads, hd).transpose(0, 2, 1, 3)

    d_qh, d_kh, d_vh = scaled_dot_product_attention_backward(d_oh, ac)
    d_q = d_qh.transpose(0, 2, 1, 3).reshape(b, t, d)
    d_k = d_kh.transpose(0, 2, 1, 3).reshape(b, t, d)
    d_v = d_vh.transpose(0, 2, 1, 3).reshape(b, t, d)

    grads["W_Q"] = x.reshape(-1, d).T @ d_q.reshape(-1, d)
    grads["b_Q"] = np.sum(d_q, axis=(0, 1))
    grads["W_K"] = x.reshape(-1, d).T @ d_k.reshape(-1, d)
    grads["b_K"] = np.sum(d_k, axis=(0, 1))
    grads["W_V"] = x.reshape(-1, d).T @ d_v.reshape(-1, d)
    grads["b_V"] = np.sum(d_v, axis=(0, 1))

    dx = d_q @ p["W_Q"].T + d_k @ p["W_K"].T + d_v @ p["W_V"].T
    return dx, grads