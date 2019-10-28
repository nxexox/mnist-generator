"""
Fonts reader

"""
from typing import Optional, Tuple

from dataclasses import dataclass
from PIL.ImageFont import FreeTypeFont as PilFreeTypeFont
from PIL import ImageFont

from mnist_generator.storage import FileReader


@dataclass
class Font(object):
    """
    Font object.

    """
    path_to_font: str
    font_size: int
    font: Optional[PilFreeTypeFont] = None

    def __post_init__(self):
        self.font = ImageFont.truetype(self.path_to_font, size=self.font_size)

    def get_text_size(self, text: str) -> Tuple[int, int]:
        """
        Get text block size.

        :param str text: Text for get size

        :return: Size text block
        :rtype: Tuple[int, int]

        """
        return self.font.getsize_multiline(text)


class FontsReader(FileReader):
    """
    Fonts reader.

    """
    def get_fonts(self, size_range):
        """
        Get fonts.

        :param Tuple[int, int] size_range: Range fot sizes fonts.

        :return: Iterable fonts
        :rtype: Generator[Font, None, None]

        """
        files_generator = self.get_files_patches_from_storage()

        for file_path in files_generator:
            for size in range(*size_range):
                yield Font(path_to_font=file_path, font_size=size)
