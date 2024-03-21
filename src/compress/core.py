from io import BufferedReader, BytesIO
from pathlib import Path

import mozjpeg_lossless_optimization
from PIL import Image


def open_and_resize_img(obj: BufferedReader, img_io: BytesIO, boundary: int = 1600):
    with Image.open(obj) as img:
        width, height = img.size
        if width > height and width > boundary:
            height = round(height * (boundary / width))
            width = boundary
        elif height > boundary:
            width = round(width * (boundary / height))
            height = boundary
        img.resize((width, height)).convert("RGB").save(
            img_io, format="JPEG", quality=90
        )
    img_io.seek(0)
    return img_io


def compress(img_io: BytesIO) -> BytesIO:
    img_io.seek(0)
    img_bytes = img_io.read()
    optimized_img_bytes = mozjpeg_lossless_optimization.optimize(img_bytes)
    img_io.flush()
    img_io.write(optimized_img_bytes)
    img_io.seek(0)
    return img_io
