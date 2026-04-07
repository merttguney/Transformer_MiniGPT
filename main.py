from __future__ import annotations
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config import GPTConfig
from train import train_model


def main():
    cfg = GPTConfig(
        d_model=128,
        n_heads=4,
        n_layers=3,
        d_ff=512,
        context_length=128,
        dropout=0.1,
        batch_size=32,
        learning_rate=3e-4,
        weight_decay=0.01,
        epochs=80,
        warmup_steps=200,
        grad_clip=1.0,
        seed=42,
        val_ratio=0.1,
    )
    print("=" * 60)
    print("  Mini GPT — Türkçe Metin Tamamlama Eğitimi")
    print("=" * 60)
    print(f"  d_model={cfg.d_model} | heads={cfg.n_heads} | layers={cfg.n_layers}")
    print(f"  d_ff={cfg.d_ff} | ctx={cfg.context_length} | dropout={cfg.dropout}")
    print(f"  lr={cfg.learning_rate} | wd={cfg.weight_decay} | epochs={cfg.epochs}")
    print("=" * 60)

    model, tok, train_losses, val_losses = train_model(cfg)

    # Örnekler
    prompts = ["Bir gün", "Sevgi", "Yol", "Sabır", "Türk dili", "İstanbul"]
    print("\n" + "=" * 60)
    print("  Örnek Çıktılar")
    print("=" * 60)
    for p in prompts:
        out = model.generate(
            tok.encode(p),
            max_tokens=120,
            temperature=0.7,
            top_k=30,
            top_p=0.9,
            eos_id=tok.eos_id,
        )
        print(f"\nPROMPT: {p}")
        print(f"ÇIKTI : {tok.decode(out)}")

    # Loss grafiği
    fig, ax = plt.subplots(figsize=(10, 5))
    epochs = range(1, len(train_losses) + 1)
    ax.plot(epochs, train_losses, color="#22d3ee", linewidth=2, label="Train Loss")
    ax.plot(epochs, val_losses, color="#f472b6", linewidth=2, label="Val Loss")
    ax.set_title("Mini GPT · Eğitim & Doğrulama Loss", fontsize=14)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig("checkpoints/loss_curve.png", dpi=150)
    print("\n[kayıt] Loss grafiği: checkpoints/loss_curve.png")
    plt.show()


if __name__ == "__main__":
    main()
