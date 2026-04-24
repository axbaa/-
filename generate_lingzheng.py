from __future__ import annotations

from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


WIDTH = 1600
HEIGHT = 2000
OUTPUT = Path("lingzheng_poster.png")
FONT_PATHS = [
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
]


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    for font_path in FONT_PATHS:
        if Path(font_path).exists():
            return ImageFont.truetype(font_path, size=size, index=0)
    return ImageFont.load_default()


def lerp_channel(start: int, end: int, ratio: float) -> int:
    return int(start + (end - start) * ratio)


def vertical_gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, top)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        ratio = y / max(height - 1, 1)
        color = tuple(lerp_channel(top[i], bottom[i], ratio) for i in range(3))
        draw.line((0, y, width, y), fill=color)
    return image


def draw_heart(draw: ImageDraw.ImageDraw, center: tuple[int, int], size: int, fill: tuple[int, int, int, int]) -> None:
    x, y = center
    radius = size // 3
    draw.ellipse((x - radius * 2, y - radius * 2, x, y), fill=fill)
    draw.ellipse((x, y - radius * 2, x + radius * 2, y), fill=fill)
    draw.polygon(
        [
            (x - radius * 2, y - radius // 2),
            (x + radius * 2, y - radius // 2),
            (x, y + size),
        ],
        fill=fill,
    )


def add_text_centered(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont, fill: tuple[int, int, int], spacing: int = 4) -> int:
    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align="center")
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    draw.multiline_text(((WIDTH - width) / 2, y), text, font=font, fill=fill, spacing=spacing, align="center")
    return y + height


def create_booklet(title: str) -> Image.Image:
    booklet = Image.new("RGBA", (360, 500), (0, 0, 0, 0))
    shadow = Image.new("RGBA", booklet.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((20, 20, 340, 470), radius=28, fill=(140, 0, 28, 180))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    booklet.alpha_composite(shadow, dest=(0, 10))

    draw = ImageDraw.Draw(booklet)
    draw.rounded_rectangle((30, 20, 330, 460), radius=28, fill=(177, 20, 39, 255), outline=(255, 218, 152, 255), width=6)
    draw.rounded_rectangle((48, 40, 312, 440), radius=22, outline=(252, 224, 168, 180), width=3)

    gold = (255, 221, 142, 255)
    star_points = [
        (180, 128),
        (196, 171),
        (241, 171),
        (205, 198),
        (219, 242),
        (180, 216),
        (141, 242),
        (155, 198),
        (119, 171),
        (164, 171),
    ]
    draw.polygon(star_points, fill=gold)

    title_font = load_font(58)
    small_font = load_font(36)
    draw.text((180, 292), title, font=title_font, fill=gold, anchor="mm")
    draw.text((180, 352), "Marriage", font=small_font, fill=(255, 235, 190, 220), anchor="mm")
    draw.text((180, 388), "Certificate", font=small_font, fill=(255, 235, 190, 220), anchor="mm")
    return booklet


def main() -> None:
    image = vertical_gradient((WIDTH, HEIGHT), (255, 247, 244), (255, 221, 232)).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    for center, size, color in [
        ((180, 180), 90, (255, 196, 210, 90)),
        ((1360, 240), 120, (255, 210, 220, 110)),
        ((150, 1660), 110, (255, 206, 218, 80)),
        ((1450, 1750), 80, (255, 187, 204, 100)),
    ]:
        overlay_draw.ellipse((center[0] - size, center[1] - size, center[0] + size, center[1] + size), fill=color)

    image = Image.alpha_composite(image, overlay)

    shadow_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_draw.rounded_rectangle((150, 170, 1450, 1830), radius=60, fill=(160, 62, 86, 55))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(24))
    image.alpha_composite(shadow_layer, dest=(0, 18))

    card = Image.new("RGBA", image.size, (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card)
    card_draw.rounded_rectangle((130, 150, 1470, 1810), radius=60, fill=(255, 252, 248, 242))
    card_draw.rounded_rectangle((160, 180, 1440, 1780), radius=48, outline=(222, 64, 98, 110), width=4)
    card_draw.rounded_rectangle((178, 198, 1422, 1762), radius=42, outline=(235, 162, 178, 80), width=2)
    image = Image.alpha_composite(image, card)

    deco = ImageDraw.Draw(image)
    gold = (186, 100, 32, 255)
    rose = (215, 64, 97, 255)
    soft = (241, 127, 149, 255)

    top_font = load_font(44)
    title_font = load_font(120)
    sub_font = load_font(52)
    note_font = load_font(34)
    seal_font = load_font(88)

    deco.text((WIDTH / 2, 280), "幸福启程", font=top_font, fill=soft, anchor="mm")
    deco.line((565, 280, 705, 280), fill=(237, 168, 180, 180), width=3)
    deco.line((895, 280, 1035, 280), fill=(237, 168, 180, 180), width=3)

    deco.text((WIDTH / 2, 410), "我们领证啦", font=title_font, fill=rose, anchor="mm")
    deco.text((WIDTH / 2, 500), "JUST MARRIED", font=sub_font, fill=(190, 108, 126, 255), anchor="mm")

    heart_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    heart_draw = ImageDraw.Draw(heart_layer)
    draw_heart(heart_draw, (610, 610), 44, (255, 142, 166, 200))
    draw_heart(heart_draw, (990, 610), 44, (255, 142, 166, 200))
    draw_heart(heart_draw, (220, 330), 38, (255, 176, 192, 160))
    draw_heart(heart_draw, (1360, 390), 38, (255, 176, 192, 160))
    draw_heart(heart_draw, (1320, 1530), 34, (255, 176, 192, 120))
    draw_heart(heart_draw, (290, 1520), 34, (255, 176, 192, 120))
    image = Image.alpha_composite(image, heart_layer)

    booklet_left = create_booklet("结婚证").rotate(-8, resample=Image.Resampling.BICUBIC, expand=True)
    booklet_right = create_booklet("结婚证").rotate(8, resample=Image.Resampling.BICUBIC, expand=True)
    image.alpha_composite(booklet_left, dest=(385, 660))
    image.alpha_composite(booklet_right, dest=(808, 660))

    deco.rounded_rectangle((290, 1290, 1310, 1510), radius=36, fill=(255, 242, 246, 255), outline=(242, 175, 191, 190), width=3)
    deco.text((800, 1354), "从今天起，合法贴贴", font=load_font(64), fill=gold, anchor="mm")
    deco.text((800, 1432), "愿每一页日常，都写满偏爱与陪伴", font=note_font, fill=(164, 118, 128, 255), anchor="mm")

    today = date.today().strftime("%Y.%m.%d")
    deco.text((800, 1608), f"领证纪念日  {today}", font=load_font(46), fill=(176, 86, 108, 255), anchor="mm")
    deco.text((800, 1680), "LOVE IS OFFICIALLY ON THE RECORD", font=load_font(30), fill=(187, 120, 136, 255), anchor="mm")

    deco.ellipse((1210, 1500, 1405, 1695), outline=(220, 85, 111, 220), width=8)
    deco.ellipse((1235, 1525, 1380, 1670), outline=(220, 85, 111, 130), width=3)
    deco.text((1307, 1598), "囍", font=seal_font, fill=(220, 85, 111, 220), anchor="mm")

    deco.arc((220, 1050, 470, 1300), 215, 328, fill=(240, 186, 198, 180), width=4)
    deco.arc((1130, 1040, 1380, 1290), 212, 325, fill=(240, 186, 198, 180), width=4)

    image = image.convert("RGB")
    image.save(OUTPUT, quality=95)
    print(f"saved {OUTPUT.resolve()}")


if __name__ == "__main__":
    main()
