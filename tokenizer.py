from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List


# Özel token sabitleri
PAD_TOKEN = "<PAD>"
UNK_TOKEN = "<UNK>"
EOS_TOKEN = "<EOS>"
SPECIAL_TOKENS = [PAD_TOKEN, UNK_TOKEN, EOS_TOKEN]


@dataclass
class CharTokenizer:
    """Karakter bazlı tokenizer — PAD / UNK / EOS desteği."""

    stoi: Dict[str, int] = field(default_factory=dict)
    itos: Dict[int, str] = field(default_factory=dict)

    # ── Factory ──
    @classmethod
    def from_text(cls, text: str) -> "CharTokenizer":
        stoi: Dict[str, int] = {}
        for tok in SPECIAL_TOKENS:
            stoi[tok] = len(stoi)
        for ch in sorted(set(text)):
            if ch not in stoi:
                stoi[ch] = len(stoi)
        itos = {i: c for c, i in stoi.items()}
        return cls(stoi=stoi, itos=itos)

    # ── Özellikler ──
    @property
    def vocab_size(self) -> int:
        return len(self.stoi)

    @property
    def pad_id(self) -> int:
        return self.stoi[PAD_TOKEN]

    @property
    def unk_id(self) -> int:
        return self.stoi[UNK_TOKEN]

    @property
    def eos_id(self) -> int:
        return self.stoi[EOS_TOKEN]

    # ── Encode / Decode ──
    def encode(self, text: str) -> List[int]:
        """Bilinmeyen karakterler UNK olarak kodlanır."""
        return [self.stoi.get(c, self.unk_id) for c in text]

    def decode(self, ids: List[int]) -> str:
        """Özel tokenlar çıktıdan filtrelenir."""
        out: List[str] = []
        for i in ids:
            tok = self.itos.get(i, "")
            if tok in SPECIAL_TOKENS:
                if tok == EOS_TOKEN:
                    break
                continue
            out.append(tok)
        return "".join(out)
