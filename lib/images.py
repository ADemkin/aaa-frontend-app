from typing import Self
from dataclasses import dataclass
from io import BytesIO
from typing import IO
from base64 import b64encode

from PIL.Image import Image
from PIL.Image import open as _open_image
from PIL.ImageDraw import Draw
from PIL.ImageDraw import ImageDraw


Coords = list[list[int]]  # EasyOCR format
Box = tuple[int, int, int, int]  # PIL format


def open_image(image_fp: IO[bytes]) -> Image:
    return _open_image(image_fp)


@dataclass(slots=True)
class PolygonDrawer:
    image: Image
    original_image: Image
    draw: ImageDraw
    text_height_px: int = 12
    color: str = "red"

    @classmethod
    def from_image(cls, image: Image) -> Self:
        return cls(
            image=image,
            original_image=image.copy(),
            draw=Draw(image),
        )

    @staticmethod
    def coords_to_box(coords: Coords) -> Box:
        """Convert EasyOCR coords to PIL box format"""
        return coords[0][0], coords[0][1], coords[2][0], coords[2][1]

    def highlight_word(self, coords: Coords, word: str) -> None:
        """Add polygon at given coords and add word"""
        box = self.coords_to_box(coords)
        self.draw.rectangle(xy=box, outline=self.color)
        x, y = box[:2]
        self.draw.text(
            xy=(x, y - self.text_height_px),
            text=word,
            fill=self.color,
        )

    def crop(self, coords: Coords) -> Image:
        """Get cropped Image part"""
        box = self.coords_to_box(coords)
        return self.original_image.crop(box)

    def get_highlighted_image(self) -> Image:
        """Get result Image with highlights"""
        return self.image


def _image_b64encode(image: Image) -> str:
    with BytesIO() as io:
        image.save(io, format="png", quality=100)
        io.seek(0)
        return b64encode(io.read()).decode()


def image_to_img_src(image: Image) -> str:
    return f"data:image/png;base64,{_image_b64encode(image)}"
