from pathlib import Path
from typing import Tuple
import colorsys


BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"
CACHE_DIR = BASE_DIR / ".cache"
CACHE_PICTURES_DIR = CACHE_DIR / "pictures"
PIXABAY_CONFIG = CONFIG_DIR / "pixabay.json"
app_name = "PotatoFocus"
icon = BASE_DIR / "resource/potota.svg"
logo_icon = icon
tray_icon = icon
DEFAULT_SCREEN_PHOTO =  BASE_DIR / "resource/ScreenPhoto/default.jpg"

# QTimer的倒计时间隔 1s=1000ms
timer_interval = 1000
# 35min
timer_work = 5 # seconds
# 5min
timer_break = 5 # seconds


def get_image_main_color(image_path: str, size: Tuple[int, int] = (200, 200))-> Tuple[int, int, int]:
    from PIL import Image
    from collections import Counter

    image = Image.open(image_path)
    # 缩小图片尺寸，减少计算量
    image = image.resize(size)
    # 将图片转换为 RGB 模式
    image = image.convert('RGB')
    # 减少颜色数量
    image = image.quantize(colors=20)
    image = image.convert('RGB')
    pixels = list(image.getdata())
    most_common_color = Counter(pixels).most_common(1)[0][0]
    return most_common_color


def get_contrast_color(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    获取对比色，确保与背景色有足够的对比度，方便作为字体颜色
    :param color: 背景色的 RGB 值
    :return: 对比色的 RGB 值
    """
    def luminance(r, g, b):
        # 计算单个颜色通道的相对亮度
        def adjust(c):
            c /= 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

    r, g, b = color
    bg_luminance = luminance(r, g, b)

    # 将 RGB 转换为 HSV
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

    # 调整色相以获取对比色
    new_h = (h + 0.5) % 1  # 在色轮上旋转 180 度

    # 根据背景亮度调整饱和度和明度
    if bg_luminance > 0.5:
        new_s = min(1, s + 0.2)
        new_v = max(0, v - 0.3)
    else:
        new_s = min(1, s + 0.2)
        new_v = min(1, v + 0.3)

    # 将 HSV 转换回 RGB
    new_r, new_g, new_b = colorsys.hsv_to_rgb(new_h, new_s, new_v)

    # 转换为 0 - 255 范围的整数
    return (int(new_r * 255), int(new_g * 255), int(new_b * 255))

