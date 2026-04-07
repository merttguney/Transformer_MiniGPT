# Mini GPT — Türkçe Metin Tamamlama

Sıfırdan NumPy ile yazılmış **Decoder-Only Transformer** modeli.
Hiçbir deep learning framework'ü (PyTorch, TensorFlow) kullanılmamıştır.

## Mimari Özellikler

| Özellik | Değer |
|---------|-------|
| Mimari | Pre-LayerNorm Decoder-Only Transformer |
| Embedding | Token + Sinüsoidal Positional Encoding |
| Attention | Multi-Head Causal Self-Attention + Dropout |
| FFN | 2-layer ReLU + Dropout |
| Optimizer | AdamW (weight decay) |
| LR Schedule | Warmup + Cosine Decay |
| Tokenizer | Karakter bazlı (PAD / UNK / EOS desteği) |
| Sampling | Top-K + Top-P (Nucleus) + Repetition Penalty |

## Kurulum (macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Eğitim

```bash
python3 main.py
```

## Web Arayüzü

```bash
python3 app.py
```

Tarayıcı: http://127.0.0.1:5052

## API

| Endpoint | Metod | Açıklama |
|----------|-------|----------|
| `/health` | GET | Sağlık kontrolü |
| `/info` | GET | Model bilgisi |
| `/generate` | POST | Metin üretimi — `{prompt, max_tokens, temperature, top_k, top_p, repetition_penalty}` |
| `/attention` | POST | Attention matrisi — `{text}` |

## Dosya Yapısı

```
├── config.py              # Konfigürasyon dataclass
├── corpus.py              # Türkçe eğitim corpus'u
├── tokenizer.py           # Karakter tokenizer (PAD/UNK/EOS)
├── embedding.py           # Positional encoding + token embedding
├── attention.py           # Scaled dot-product + Multi-head attention
├── transformer_block.py   # Pre-LN Transformer block
├── gpt.py                 # Ana GPT modeli
├── train.py               # Eğitim pipeline (AdamW, LR schedule, grad clip)
├── app.py                 # Flask web sunucusu
├── main.py                # Eğitim başlatıcı
├── static/index.html      # Web arayüzü
└── checkpoints/           # Kaydedilen model ve metadata
```
