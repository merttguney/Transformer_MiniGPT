from __future__ import annotations
from dataclasses import dataclass, asdict
import json


@dataclass
class GPTConfig:
    """Model ve eğitim konfigürasyonu."""

    # ── Model ──
    vocab_size: int = 80
    d_model: int = 128
    n_heads: int = 4
    n_layers: int = 3
    d_ff: int = 512
    context_length: int = 128
    dropout: float = 0.1

    # ── Eğitim ──
    batch_size: int = 32
    learning_rate: float = 3e-4
    weight_decay: float = 0.01
    epochs: int = 80
    warmup_steps: int = 200
    grad_clip: float = 1.0
    seed: int = 42
    val_ratio: float = 0.1

    def save(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str) -> "GPTConfig":
        with open(path, "r", encoding="utf-8") as f:
            return cls(**json.load(f))
