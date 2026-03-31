#!/usr/bin/env python3
"""Generate assets/og-image.png directly with Pillow."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1200
HEIGHT = 630
BG = "#0a0a0f"
BG_2 = "#18181b"
GOLD = "#d4af37"
GOLD_2 = "#b8972e"
WHITE = "#ffffff"
MUTED = "#a1a1aa"
SUBTLE = "#71717a"


def load_font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        if bold
        else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_gradient(draw: ImageDraw.ImageDraw):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = blend_hex(BG, BG_2, ratio)
        draw.line((0, y, WIDTH, y), fill=color)


def blend_hex(a: str, b: str, ratio: float) -> tuple[int, int, int]:
    av = tuple(int(a[i : i + 2], 16) for i in (1, 3, 5))
    bv = tuple(int(b[i : i + 2], 16) for i in (1, 3, 5))
    return tuple(int(av[i] + (bv[i] - av[i]) * ratio) for i in range(3))


def draw_glow(
    image: Image.Image, center: tuple[int, int], radius: int, color: str, alpha: int
):
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    rgb = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))
    for step in range(radius, 0, -20):
        current_alpha = int(alpha * (step / radius) ** 2)
        overlay_draw.ellipse(
            (center[0] - step, center[1] - step, center[0] + step, center[1] + step),
            fill=rgb + (current_alpha,),
        )
    image.alpha_composite(overlay)


def draw_centered(draw, text, y, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (WIDTH - (bbox[2] - bbox[0])) / 2
    draw.text((x, y), text, font=font, fill=fill)


def main():
    assets_dir = Path(__file__).resolve().parents[1] / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    output = assets_dir / "og-image.png"

    image = Image.new("RGBA", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    draw_gradient(draw)
    draw_glow(image, (1100, -30), 280, GOLD, 70)
    draw_glow(image, (120, 700), 220, GOLD, 45)

    for x in range(0, WIDTH, 50):
        draw.line((x, 0, x, HEIGHT), fill=(212, 175, 55, 10), width=1)
    for y in range(0, HEIGHT, 50):
        draw.line((0, y, WIDTH, y), fill=(212, 175, 55, 10), width=1)

    title_font = load_font(64, bold=True)
    subtitle_font = load_font(26)
    brand_font = load_font(28, bold=True)
    pill_font = load_font(16, bold=True)
    cta_font = load_font(18, bold=True)
    url_font = load_font(14)

    draw.rounded_rectangle((500, 92, 556, 148), radius=12, fill=GOLD)
    draw_centered(draw, "N", 103, load_font(32, bold=True), BG)
    draw_centered(draw, "NeuroSkills", 154, brand_font, WHITE)

    draw_centered(draw, "O Bastidor Técnico", 215, title_font, WHITE)
    draw_centered(draw, "que o Mercado Não Mostra", 290, title_font, GOLD)
    draw_centered(
        draw, "Framework de automação de Meta Ads para", 392, subtitle_font, MUTED
    )
    draw_centered(
        draw, "Claude Code, OpenAI Codex e Gemini CLI", 426, subtitle_font, MUTED
    )

    pills = ["Skills Prontos", "Automação Real", "ROI Comprovado"]
    pill_width = 240
    gap = 20
    total = (pill_width * len(pills)) + (gap * (len(pills) - 1))
    start_x = (WIDTH - total) // 2
    y = 480
    for index, label in enumerate(pills):
        x = start_x + index * (pill_width + gap)
        draw.rounded_rectangle(
            (x, y, x + pill_width, y + 42),
            radius=21,
            fill=(255, 255, 255, 12),
            outline=(212, 175, 55, 50),
            width=1,
        )
        draw.ellipse((x + 12, y + 11, x + 32, y + 31), fill=GOLD)
        draw.text((x + 20, y + 14), "•", font=load_font(12, bold=True), fill=BG)
        draw.text((x + 42, y + 12), label, font=pill_font, fill=WHITE)

    cta_x1, cta_y1, cta_x2, cta_y2 = 430, 548, 770, 598
    draw.rounded_rectangle((cta_x1, cta_y1, cta_x2, cta_y2), radius=25, fill=GOLD_2)
    draw_centered(draw, "Começar Agora ->", 561, cta_font, BG)
    draw_centered(draw, "goldneuron.io", 607, url_font, SUBTLE)

    image.convert("RGB").save(output, "PNG")
    print(f"Generated {output}")


if __name__ == "__main__":
    main()
