#!/usr/bin/env python3
from pathlib import Path
import sys
from PIL import Image

# ─── HARDCODED CARD SIZE ───────────────────────────────────
CARD_W, CARD_H = 856, 1200
# Desired output DPI
OUT_DPI = (96, 96)
# ───────────────────────────────────────────────────────────

def main():
    base    = Path(__file__).parent.resolve()
    src_dir = base / "src"
    out_dir = base / "out"

    if not src_dir.is_dir():
        print(f"✗ Couldn’t find src/ at {src_dir}")
        sys.exit(1)

    pngs = sorted(src_dir.rglob("*.png"))
    if not pngs:
        print(f"✗ No PNGs found in {src_dir}")
        sys.exit(1)

    for p in pngs:
        rel_path = p.relative_to(src_dir)
        out_path = out_dir / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # convert Path to str for width formatting
        print(f"Processing {str(rel_path):35}", end=" ")

        with Image.open(p).convert("RGBA") as src_img:
            # simple resize (distorts to fit the exact CARD_W×CARD_H)
            resized = src_img.resize((CARD_W, CARD_H), Image.LANCZOS)
            resized.save(out_path, dpi=OUT_DPI)

        print("✔")

    print("\n✅ Done! Check:\n  • out/   (cards at 856×1200, 96 DPI)")

if __name__ == "__main__":
    main()
