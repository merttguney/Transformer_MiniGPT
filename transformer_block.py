from __future__ import annotations
import numpy as np
from typing import Dict
from attention import (
    multi_head_attention_forward,
    multi_head_attention_backward,
    dropout_forward,
    dropout_backward,
)


def he_init(fan_in: int, fan_out: int) -> np.ndarray:
    return np.random.randn(fan_in, fan_out).astype(np.float32) * np.sqrt(2.0 / fan_in)


# ────────────────────────────────────────
# Layer Normalization
# ────────────────────────────────────────

def layer_norm_forward(x: np.ndarray, gamma: np.ndarray, beta: np.ndarray, eps: float = 1e-5):
    mu = np.mean(x, axis=-1, keepdims=True)
    var = np.var(x, axis=-1, keepdims=True)
    xh = (x - mu) / np.sqrt(var + eps)
    y = gamma * xh + beta
    return y, {"x": x, "xh": xh, "var": var, "gamma": gamma, "eps": eps}


def layer_norm_backward(dy: np.ndarray, c: Dict):
    x, xh, var, gamma, eps = c["x"], c["xh"], c["var"], c["gamma"], c["eps"]
    n = x.shape[-1]
    d_gamma = np.sum(dy * xh, axis=tuple(range(len(dy.shape) - 1)))
    d_beta = np.sum(dy, axis=tuple(range(len(dy.shape) - 1)))
    dxh = dy * gamma
    inv = 1.0 / np.sqrt(var + eps)
    dx = (1.0 / n) * inv * (
        n * dxh
        - np.sum(dxh, axis=-1, keepdims=True)
        - xh * np.sum(dxh * xh, axis=-1, keepdims=True)
    )
    return dx, d_gamma, d_beta


# ────────────────────────────────────────
# Feed-Forward Network (ReLU)
# ────────────────────────────────────────

def ffn_forward(x: np.ndarray, p: Dict):
    h = x @ p["W1"] + p["b1"]
    a = np.maximum(0, h)
    y = a @ p["W2"] + p["b2"]
    return y, {"x": x, "h": h, "a": a}


def ffn_backward(dy: np.ndarray, c: Dict, p: Dict):
    x, h, a = c["x"], c["h"], c["a"]
    d = x.shape[-1]
    g = {k: np.zeros_like(v) for k, v in p.items()}
    g["W2"] = a.reshape(-1, a.shape[-1]).T @ dy.reshape(-1, dy.shape[-1])
    g["b2"] = np.sum(dy, axis=tuple(range(len(dy.shape) - 1)))
    da = dy @ p["W2"].T
    dh = da * (h > 0).astype(np.float32)
    g["W1"] = x.reshape(-1, d).T @ dh.reshape(-1, dh.shape[-1])
    g["b1"] = np.sum(dh, axis=tuple(range(len(dh.shape) - 1)))
    dx = dh @ p["W1"].T
    return dx, g


# ────────────────────────────────────────
# Transformer Block — Pre-LayerNorm
# ────────────────────────────────────────

class TransformerBlock:
    def __init__(self, d_model: int, n_heads: int, d_ff: int, dropout: float = 0.1):
        self.n_heads = n_heads
        self.dropout = dropout
        self.params: Dict[str, np.ndarray] = {
            # Attention
            "W_Q": he_init(d_model, d_model), "b_Q": np.zeros((d_model,), np.float32),
            "W_K": he_init(d_model, d_model), "b_K": np.zeros((d_model,), np.float32),
            "W_V": he_init(d_model, d_model), "b_V": np.zeros((d_model,), np.float32),
            "W_O": he_init(d_model, d_model), "b_O": np.zeros((d_model,), np.float32),
            # LayerNorm 1
            "ln1_gamma": np.ones((d_model,), np.float32),
            "ln1_beta": np.zeros((d_model,), np.float32),
            # FFN
            "W1": he_init(d_model, d_ff), "b1": np.zeros((d_ff,), np.float32),
            "W2": he_init(d_ff, d_model), "b2": np.zeros((d_model,), np.float32),
            # LayerNorm 2
            "ln2_gamma": np.ones((d_model,), np.float32),
            "ln2_beta": np.zeros((d_model,), np.float32),
        }
        self.grads: Dict[str, np.ndarray] = {k: np.zeros_like(v) for k, v in self.params.items()}

    # ── Forward (Pre-LN) ──
    def forward(self, x: np.ndarray, mask: np.ndarray, training: bool = False):
        # LN1 → Attention → residual dropout → add
        n1, c1 = layer_norm_forward(x, self.params["ln1_gamma"], self.params["ln1_beta"])
        ap = {k: self.params[k] for k in ["W_Q", "b_Q", "W_K", "b_K", "W_V", "b_V", "W_O", "b_O"]}
        attn_out, aw, ac = multi_head_attention_forward(n1, ap, self.n_heads, mask, self.dropout, training)
        attn_out, rd1 = dropout_forward(attn_out, self.dropout, training)
        h = x + attn_out

        # LN2 → FFN → residual dropout → add
        n2, c2 = layer_norm_forward(h, self.params["ln2_gamma"], self.params["ln2_beta"])
        fp = {k: self.params[k] for k in ["W1", "b1", "W2", "b2"]}
        f, fc = ffn_forward(n2, fp)
        f, rd2 = dropout_forward(f, self.dropout, training)
        out = h + f

        cache = {"x": x, "h": h, "c1": c1, "ac": ac, "c2": c2, "fc": fc, "rd1": rd1, "rd2": rd2}
        return out, aw, cache

    # ── Backward (Pre-LN) ──
    def backward(self, dout: np.ndarray, c: Dict):
        for k in self.grads:
            self.grads[k].fill(0.0)

        # out = h + dropout(FFN(LN2(h)))
        dh_res = dout
        df = dropout_backward(dout, c["rd2"])

        fp = {k: self.params[k] for k in ["W1", "b1", "W2", "b2"]}
        dn2, fg = ffn_backward(df, c["fc"], fp)
        for k, v in fg.items():
            self.grads[k] += v

        dh_ln2, g2, b2 = layer_norm_backward(dn2, c["c2"])
        self.grads["ln2_gamma"] += g2
        self.grads["ln2_beta"] += b2

        dh = dh_res + dh_ln2

        # h = x + dropout(Attention(LN1(x)))
        dx_res = dh
        d_attn = dropout_backward(dh, c["rd1"])

        ap = {k: self.params[k] for k in ["W_Q", "b_Q", "W_K", "b_K", "W_V", "b_V", "W_O", "b_O"]}
        dn1, ag = multi_head_attention_backward(d_attn, c["ac"], ap)
        for k, v in ag.items():
            self.grads[k] += v

        dx_ln1, g1, b1 = layer_norm_backward(dn1, c["c1"])
        self.grads["ln1_gamma"] += g1
        self.grads["ln1_beta"] += b1

        return dx_res + dx_ln1
