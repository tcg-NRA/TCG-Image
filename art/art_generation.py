#!/usr/bin/env python3
from pathlib import Path
import sys
from PIL import Image

# ─── HARDCODED SIZES ───────────────────────────────────────
CARD_W, CARD_H   = 856, 1200
BOARD_W, BOARD_H = 856, 836
# ───────────────────────────────────────────────────────────

def match_cover(img: Image.Image, tw: int, th: int) -> Image.Image:
    scale = max(tw / img.width, th / img.height)
    nw, nh = int(img.width * scale), int(img.height * scale)
    resized = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top  = (nh - th) // 2
    return resized.crop((left, top, left + tw, top + th))

def match_cover_offset(img: Image.Image, tw: int, th: int, frac: float = 0.1) -> Image.Image:
    scale = max(tw / img.width, th / img.height)
    nw, nh = int(img.width * scale), int(img.height * scale)
    resized = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    overflow = nh - th
    top = int(overflow * frac)
    top = max(0, min(top, overflow))
    return resized.crop((left, top, left + tw, top + th))

def main():
    base       = Path(__file__).parent.resolve()
    src_dir    = base / "src"
    out_dir    = base / "out"
    out_board  = base / "out_board"

    if not src_dir.is_dir():
        print(f"✗ Couldn’t find src/ at {src_dir}")
        sys.exit(1)

    # Recursively find PNGs
    pngs = sorted(src_dir.rglob("*.png"))
    if not pngs:
        print(f"✗ No PNGs found in {src_dir}")
        sys.exit(1)

    for p in pngs:
        rel_path = p.relative_to(src_dir)
        out_path = out_dir / rel_path
        board_path = out_board / rel_path.parent / (p.stem + "_board.png")

        # Make sure output folders exist
        out_path.parent.mkdir(parents=True, exist_ok=True)
        board_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Processing {str(rel_path):35}", end=" ")

        with Image.open(p).convert("RGBA") as src_img:
            # card version (856×1200)
            card_img = match_cover(src_img, CARD_W, CARD_H)
            card_img.save(out_path)

            # board version (856×836) with 10% top-offset
            board_img = match_cover_offset(src_img, BOARD_W, BOARD_H, frac=0.1)
            board_img.save(board_path)

        print("✔")

    print("\n✅ Done! Check:\n  • out/       (cards at 856×1200)\n  • out_board/ (boards at 856×836)")

if __name__ == "__main__":
    main()