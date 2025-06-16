import os
from PIL import Image
import numpy as np

# ─── CONFIG ────────────────────────────────────────────────────────────
BASE_DIR       = "card_frame/cropped"
SRC_DIR        = os.path.join(BASE_DIR, "src")
REF_PATH       = os.path.join(BASE_DIR, "reference", "reference.png.png")
OUT_DIR        = os.path.join(BASE_DIR, "out")
ALPHA_MIN      = 16    # alpha ≥ this is “frame”; tweak if needed
# ────────────────────────────────────────────────────────────────────────

os.makedirs(OUT_DIR, exist_ok=True)

def frame_bbox(im):
    """
    Return (x0,y0,x1,y1) of the *non-transparent* frame pixels.
    """
    arr = np.array(im.convert("RGBA"))
    alpha = arr[:, :, 3]
    mask = alpha >= ALPHA_MIN
    ys, xs = np.where(mask)
    if not len(xs):
        raise ValueError("No opaque pixels found")
    return xs.min(), ys.min(), xs.max(), ys.max()

# 1) load & measure the REFERENCE
ref_im = Image.open(REF_PATH).convert("RGBA")
ref_w, ref_h = ref_im.size
rx0, ry0, rx1, ry1 = frame_bbox(ref_im)
ref_frame_w = rx1 - rx0 + 1
ref_frame_h = ry1 - ry0 + 1

print(f"Reference canvas: {(ref_w,ref_h)}, frame box: {(rx0,ry0,rx1,ry1)}, size: {(ref_frame_w,ref_frame_h)}")

# 2) process each source
for fn in sorted(os.listdir(SRC_DIR)):
    if not fn.lower().endswith(".png"):
        continue

    src = Image.open(os.path.join(SRC_DIR, fn)).convert("RGBA")
    sx0, sy0, sx1, sy1 = frame_bbox(src)
    src_frame_w = sx1 - sx0 + 1
    src_frame_h = sy1 - sy0 + 1

    # uniform scale so that source frame width matches reference
    scale = ref_frame_w / src_frame_w

    new_size = (int(src.width * scale), int(src.height * scale))
    resized = src.resize(new_size, Image.LANCZOS)

    # 3) center on ref-sized canvas
    canvas = Image.new("RGBA", (ref_w, ref_h), (0,0,0,0))
    off_x = (ref_w  - new_size[0]) // 2
    off_y = (ref_h  - new_size[1]) // 2
    canvas.paste(resized, (off_x, off_y), resized)

    out_path = os.path.join(OUT_DIR, fn)
    canvas.save(out_path)
    print(f"{fn}: frame {src_frame_w}×{src_frame_h} → scaled {new_size} → saved to out/")
