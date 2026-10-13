
from PIL import Image
from PIL import ImageOps
import os

INPUT_IMAGE = "Neon ASCII Portrait with Cross Pendant.png"
OUTPUT_GIF = "portrait_line_by_line.gif"

if not os.path.exists(INPUT_IMAGE):
    raise FileNotFoundError(
        f"Image not found: {INPUT_IMAGE}\n"
        "Download the image and run this script in the same folder."
    )

image = Image.open(INPUT_IMAGE).convert("RGB")
image.thumbnail((700, 700))

width, height = image.size
frames = []

# Reveal the portrait gradually from top to bottom.
steps = 40

for step in range(1, steps + 1):
    visible_height = max(1, int(height * step / steps))
    frame = Image.new("RGB", (width, height), (8, 12, 20))
    frame.paste(image.crop((0, 0, width, visible_height)), (0, 0))
    frames.append(frame)

frames[0].save(
    OUTPUT_GIF,
    save_all=True,
    append_images=frames[1:],
    duration=70,
    loop=0,
    optimize=False
)

print(f"Created {OUTPUT_GIF}")

