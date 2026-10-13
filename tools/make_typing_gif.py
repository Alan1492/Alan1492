#!/usr/bin/env python3
"""
make_typing_gif.py
Create a black-background ASCII typing animation from a text art file.

Usage:
  python make_typing_gif.py ascii-art.txt typing.gif --font "DejaVuSansMono.ttf" --font-size 12 --fps 30 --step 2

Requirements:
  pip install pillow imageio
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio


def load_ascii(path: str, max_cols: int | None = None):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    if not lines:
        raise ValueError("ASCII file is empty.")
    width = max(len(line) for line in lines)
    if max_cols is not None:
        width = min(width, max_cols)
    padded = [line[:width].ljust(width) for line in lines]
    return padded, width, len(padded)


def make_frame(lines, reveal_chars, font, fg=(255, 255, 255), bg=(0, 0, 0), padding=10):
    rows = len(lines)
    cols = max(len(line) for line in lines) if lines else 0
    sample = "M"
    char_w = font.getbbox(sample)[2] - font.getbbox(sample)[0]
    char_h = font.getbbox(sample)[3] - font.getbbox(sample)[1]
    canvas_w = cols * char_w + padding * 2
    canvas_h = rows * char_h + padding * 2
    img = Image.new("RGB", (canvas_w, canvas_h), bg)
    draw = ImageDraw.Draw(img)

    idx = 0
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if idx >= reveal_chars:
                break
            x = padding + c * char_w
            y = padding + r * char_h
            draw.text((x, y), ch, font=font, fill=fg)
            idx += 1
        if idx >= reveal_chars:
            break
    return img


def create_typing_gif(input_path: str, output_path: str, font_path: str, font_size: int = 12, fps: int = 30, step: int = 2, bg=(0, 0, 0), fg=(255, 255, 255)):
    lines, width, height = load_ascii(input_path)
    font = ImageFont.truetype(font_path, font_size)
    total_chars = width * height
    frames = []
    durations = []

    for reveal in range(1, total_chars + 1, step):
        frame = make_frame(lines, reveal, font, fg=fg, bg=bg)
        frames.append(frame)
        durations.append(int(1000 / fps))

    # Add a brief pause at the end.
    for _ in range(max(1, int(fps * 0.6))):
        frames.append(frames[-1])
        durations.append(int(1000 / fps))

    imageio.mimsave(output_path, frames, duration=[d / 1000 for d in durations])
    print(f"Saved GIF to: {output_path}")
    print(f"Total frames: {len(frames)} | FPS: {fps} | step: {step}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reveal an ASCII portrait like a terminal painting itself in black background.")
    parser.add_argument("input", help="ASCII text file")
    parser.add_argument("output", help="Output GIF path")
    parser.add_argument("--font", default="DejaVuSansMono.ttf", help="Path to a monospaced font")
    parser.add_argument("--font-size", type=int, default=12, help="Font size")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second")
    parser.add_argument("--step", type=int, default=2, help="Characters revealed per frame")
    parser.add_argument("--bg", default="000000", help="Background color as hex")
    parser.add_argument("--fg", default="ffffff", help="Foreground color as hex")
    args = parser.parse_args()

    bg = tuple(int(args.bg[i:i+2], 16) for i in (0, 2, 4))
    fg = tuple(int(args.fg[i:i+2], 16) for i in (0, 2, 4))

    create_typing_gif(args.input, args.output, args.font, font_size=args.font_size, fps=args.fps, step=args.step, bg=bg, fg=fg)
