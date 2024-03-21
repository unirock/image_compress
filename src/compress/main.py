from concurrent.futures import ProcessPoolExecutor
from functools import partial, wraps
from io import BytesIO
from pathlib import Path
from time import perf_counter

from PIL import UnidentifiedImageError

from .core import compress, open_and_resize_img


def timeit(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        res = fn(*args, **kwargs)
        end = perf_counter()
        delta = end - start
        print(f"Выполнено за: {delta:.2f} с.")
        return res

    return wrapper


def get_images(root: Path):
    if not root.is_dir():
        raise ValueError()
    for element in root.iterdir():
        if element.is_dir():
            yield from get_images(element)
        else:
            yield element


def _process(path: Path, save_path: Path):
    with path.open("rb") as img:
        with BytesIO() as img_io:
            open_and_resize_img(img, img_io)
            compress(img_io)
            with save_path.open("wb") as result_img:
                result_img.write(img_io.read())


def process(base_root: Path, result_root: Path, image_path: Path):
    new_path = result_root / image_path.relative_to(base_root).with_suffix(
        ".jpg"
    )
    new_path.parent.mkdir(exist_ok=True, parents=True)
    try:
        _process(image_path, new_path)
    except UnidentifiedImageError:
        return


@timeit
def with_pool(base_root: Path, result_root: Path):
    partial_process = partial(process, base_root, result_root)
    with ProcessPoolExecutor() as pool:
        list(pool.map(partial_process, get_images(base_root)))


@timeit
def with_loop(base_root: Path, result_root: Path):
    partial_process = partial(process, base_root, result_root)
    for img_path in get_images(base_root):
        partial_process(img_path)


# @timeit
# def main():
#     path = Path("/home/kiortir/dev/unirock_image_crop/demo")
#     result_path = path / "result/"
#     with_pool(path, result_path)


# if __name__ == "__main__":
#     main()
