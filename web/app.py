"""Flask web sunucusu — Mini GPT Türkçe Metin Tamamlama."""
from __future__ import annotations
import json, os, sys, traceback

# Proje kökünü Python path'ine ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
from flask import Flask, jsonify, request, send_from_directory

from data.tokenizer import CharTokenizer
from model.gpt import GPT

# static klasörü web/ altında
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), "static"))

MODEL: GPT | None = None
TOKENIZER: CharTokenizer | None = None
INFO: dict | None = None

# checkpoints/ proje kökünde
_ROOT = os.path.dirname(os.path.dirname(__file__))
_CKPT = os.path.join(_ROOT, "checkpoints")


def load_artifacts():
    global MODEL, TOKENIZER, INFO
    print("[boot] tokenizer yükleniyor...")
    with open(os.path.join(_CKPT, "tokenizer.json"), "r", encoding="utf-8") as f:
        stoi = json.load(f)["stoi"]
    TOKENIZER = CharTokenizer(stoi=stoi, itos={int(v): k for k, v in stoi.items()})

    print("[boot] train_info yükleniyor...")
    with open(os.path.join(_CKPT, "train_info.json"), "r", encoding="utf-8") as f:
        INFO = json.load(f)

    print("[boot] model ağırlıkları yükleniyor...")
    MODEL = GPT(
        INFO["vocab_size"],
        INFO["d_model"],
        INFO["n_heads"],
        INFO["n_layers"],
        INFO["d_ff"],
        INFO["context_length"],
        INFO.get("dropout", 0.1),
    )
    MODEL.load_state_dict(dict(np.load(os.path.join(_CKPT, "mini_gpt.npz"))))
    print(f"[boot] tamam — {MODEL.num_parameters():,} parametre yüklendi.")


# ── Routes ──

@app.route("/health")
def health():
    return jsonify({"ok": True})


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/info")
def info():
    return jsonify(INFO)


@app.route("/generate", methods=["POST"])
def generate():
    try:
        d = request.get_json(force=True) or {}
        prompt = str(d.get("prompt", ""))
        max_tokens = min(int(d.get("max_tokens", 80)), 500)
        temperature = max(0.01, float(d.get("temperature", 0.55)))
        top_k = int(d.get("top_k", 20))
        top_p = float(d.get("top_p", 0.9))
        repetition_penalty = float(d.get("repetition_penalty", 0.15))

        ids = TOKENIZER.encode(prompt)
        if not ids:
            return jsonify({"text": prompt, "generated": ""})

        out = MODEL.generate(
            ids,
            max_tokens=max_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            eos_id=TOKENIZER.eos_id,
        )
        new_ids = out[len(ids):]
        generated = TOKENIZER.decode(new_ids)
        return jsonify({"text": prompt + generated, "generated": generated})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/attention", methods=["POST"])
def attention():
    try:
        d = request.get_json(force=True) or {}
        text = str(d.get("text", ""))
        ids = TOKENIZER.encode(text)
        if len(ids) < 2:
            return jsonify({"tokens": list(text), "matrix": [[1.0]]})
        mat = MODEL.attention_matrix(ids).tolist()
        toks = [TOKENIZER.itos.get(i, "?") for i in ids[-MODEL.context_length:]]
        return jsonify({"tokens": toks, "matrix": mat})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    load_artifacts()
    app.run(host="0.0.0.0", port=5052, debug=False)
