from __future__ import annotations
import numpy as np
from typing import Dict, Tuple


def positional_encoding(seq_len: int, d_model: int) -> np.ndarray:
    """
    Sinüs/kosinüs positional encoding:
    PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
    """
    pe = np.zeros((seq_len, d_model), dtype=np.float32)
    position = np.arange(seq_len, dtype=np.float32)[:, None]
    div_term = np.exp(
        np.arange(0, d_model, 2, dtype=np.float32) * (-np.log(10000.0) / d_model)
    )
    pe[:, 0::2] = np.sin(position * div_term)
    pe[:, 1::2] = np.cos(position * div_term)
    return pe


def embedding_forward(
    token_ids: np.ndarray,
    token_embedding: np.ndarray,
    pos_encoding: np.ndarray,
) -> Tuple[np.ndarray, Dict]:
    """x = E[token_ids] + PE"""
    _, t = token_ids.shape
    x = token_embedding[token_ids] + pos_encoding[:t][None, :, :]
    cache = {"token_ids": token_ids, "t": t}
    return x, cache


def embedding_backward(
    dx: np.ndarray,
    cache: Dict,
    token_embedding: np.ndarray,
) -> np.ndarray:
    """dE[token] += dx"""
    d_token_embedding = np.zeros_like(token_embedding)
    token_ids = cache["token_ids"]
    np.add.at(d_token_embedding, token_ids, dx)
    return d_token_embedding