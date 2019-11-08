"""
Algorithm for full iteration:
 -> Backgrounds
 -> Texts
 -> Fonts and fonts sized
 -> Colors

"""
import mimetypes
from datetime import datetime
from typing import Optional, Tuple, Generator, List, Dict, Union, Any

from dataclasses import dataclass
from PIL import Image

from mnist_generator.background import AbstractBackgrounds
from mnist_generator.image import TextToImageWriter
from mnist_generator.storage import FileReader, FileWriter
from mnist_generator.colors import ColorsReader, Color
from mnist_generator.fonts import FontsReader, Font
from mnist_generator.texts import (
    AbstractTextParser, TextGeneratorParser,
    TEXT_PARSER_SENTENCES_MODE, ALLOWED_TEXT_PARSE_MODES
)

from .base import BaseAlgorithm
from .packaging import BasePackagingAlgorithm, RectanglePosition


@dataclass
class BTFCImage(object):
    img: Image
    color: Color
    font: Font
    filename: str


class BTFC(BaseAlgorithm):
    """
    Algorithm for full iteration:
     -> Backgrounds
     -> Texts
     -> Fonts and fonts sized
     -> Colors

    """
    text_parser_class: AbstractTextParser = TextGeneratorParser

    def __init__(self, background_reader: AbstractBackgrounds, text_reader: FileReader,
                 fonts_reader: FontsReader, color_reader: ColorsReader,
                 image_saver: FileWriter, text_to_image_write_algorithm: TextToImageWriter,
                 packing_algorithm: BasePackagingAlgorithm,
                 text_parser_class: Optional[AbstractTextParser] = None,
                 font_size_range: Tuple[int, int] = (10, 14),
                 parse_mode: str = TEXT_PARSER_SENTENCES_MODE):
        """
        Algorithm for full iteration:
         -> Backgrounds
         -> Texts
         -> Fonts and fonts sized
         -> Colors

        :param AbstractBackgrounds background_reader: Backgrounds class
        :param FileReader text_reader: Reader texts
        :param FontsReader fonts_reader: Reader fonts
        :param ColorsReader color_reader: Colors reader
        :param FileWriter image_saver: Image saver for save result images.
        :param TextToImageWriter text_to_image_write_algorithm: Algo write text to image.
        :param BasePackagingAlgorithm packing_algorithm: Algorithm for get texts positions.
        :param Optional[AbstractTextParser] text_parser_class: Text parser class.
        :param Tuple[int, int] font_size_range: Font size range [start, end]
        :param str parse_mode: Text parse mode

        """
        self._backgrounds_reader = background_reader
        self._text_reader = text_reader
        self._fonts_reader = fonts_reader
        self._color_reader = color_reader
        self._image_saver = image_saver
        self._text_to_image_write_algorithm = text_to_image_write_algorithm
        self.text_parser_class = text_parser_class or self.text_parser_class
        self._packing_algorithm = packing_algorithm
        if parse_mode not in ALLOWED_TEXT_PARSE_MODES:
            raise ValueError('parse_mode not valid value. Valid: {}'.format(ALLOWED_TEXT_PARSE_MODES))
        self._parse_mode = parse_mode
        if (len(font_size_range) != 2
                and not isinstance(font_size_range[0], int)
                and not isinstance(font_size_range[1], int)):
            raise ValueError('font_size_range not valid value. Valid: Tuple[int, int]')

        self._font_size_range = font_size_range

    def get_result_file_name(self, src_image: Image.Image) -> str:
        """
        Get result filename.

        :param PIL.Image.Image src_image: Src background image

        :return: Result filename
        :rtype: str

        """
        return 'btfc-{date}{extension}'.format(
            date=datetime.now().isoformat(),
            extension='.{}'.format(src_image.format.lower())
        )

    def _get_image_for_write(self, src_image: Image.Image) -> Image.Image:
        """
        Get image for write text to image from src image.

        :param PIL.Image.Image src_image: Source background image

        :return: Image for write text
        :rtype: PIL.Image.Image

        """
        img = src_image.copy()
        # if img.mode != 'RGBA':
        #     img = img.convert('RGBA')
        img.format = src_image.format
        return img

    def main_generator(self) -> Generator[Tuple[int, Image.Image, List[str], Font], None, None]:
        """
        Get main generator.

        :return: Main generator for main cycle. Tuple[count_iters, current_background, text_blocks, font]
        :rtype: Generator[Tuple[int, Image.Image, List[str], Font], None, None]

        """
        count_iters = len(self._backgrounds_reader.reader) + len(self._text_reader) + len(self._fonts_reader)

        for background in self._backgrounds_reader.reader.images_from_storage_generator():
            for text_file in self._text_reader.get_files_from_storage():

                text_blocks = list(self.text_parser_class.get_text_blocks(text_file, mode=self._parse_mode,
                                                                          added_separator=True))
                for font in self._fonts_reader.get_fonts(self._font_size_range):
                    yield count_iters, background, text_blocks, font

    def get_base_images(self, background: Image.Image,
                        font: Font) -> Dict[Tuple[int, int, int], Union[List[BTFCImage], BTFCImage]]:
        """
        Get images for write.

        :param Image.Image background: Background
        :param Font font: Font for calculate.

        :return: Images dict for write.
        :rtype: Dict[Tuple[int, int, int], Union[List[BTFCImage], BTFCImage]]

        """
        return {
            color.to_tuple(): BTFCImage(
                img=self._get_image_for_write(background), color=color,
                font=font, filename=self.get_result_file_name(background)
            )
            for color in self._color_reader.get_colors()
        }

    def calculate_text_blocks(self, src_text_blocks: List[str], font: Font,
                              background: Image.Image) -> List[RectanglePosition]:
        """
        Calculate text blocks.

        :param List[str] src_text_blocks: Src text blocks.
        :param Font font: Font for calculate.
        :param Image.Image background: Background for calculate size

        :return: Calculations text blocks positions
        :rtype: List[RectanglePosition]

        """
        # Processing text blocks for calculate
        text_blocks_sized = [
            font.get_text_size(text_block) + (text_block,)
            for text_block in src_text_blocks
        ]
        text_blocks_rectangles = self._packing_algorithm.create_rectangles(text_blocks_sized)
        # text_blocks_rectangles_index = {rec.rectangle_id: rec for rec in text_blocks_rectangles}
        holst = self._packing_algorithm.create_holst(*background.size)

        # Calculate
        text_block_positions = self._packing_algorithm.packing(holst=holst,
                                                               rectangles=text_blocks_rectangles)
        #
        # # Processing text blocks for write
        # text_blocks_for_write = [
        #     (text_blocks_rectangles_index.get(rec_position.rectangle.rectangle_id), rec_position)
        #     for rec_position in text_block_positions
        # ]

        return text_block_positions

    def iterator_by_images(self, key: Any,
                           images: Dict[Tuple[int, int, int], Union[List[BTFCImage], BTFCImage]]) \
            -> Generator[BTFCImage, None, None]:
        """
        Iterator by images.

        :param Any key: Key for get images
        :param Dict[Tuple[int, int, int], Union[List[BTFCImage], BTFCImage]] images: Images for get iterator

        :return: Generator[BTFCImage, None, None]

        """
        yield images[key]

    def image_post_process(self, img: BTFCImage) -> BTFCImage:
        """
        Post processing image after save to storage.

        :param Image.Image img: Image for processing.

        :return: Processing image
        :rtype: BTFCImage

        """
        return img

    def save_image(self, img: BTFCImage):
        """
        Save image to storage.

        :param BTFCImage img: Image for save to storage.

        """
        # Get result filename
        self._image_saver.write(img.filename, img.img)

    def run(self, verbose: bool = False):
        """
        Run BTFC algorithm.

        :param bool verbose: Verbose debug messages?

        """
        index = 0
        count_colors = len(self._color_reader)

        for count_iters, background, text_blocks, font in self.main_generator():
            images = self.get_base_images(background, font)
            text_blocks_for_write = self.calculate_text_blocks(text_blocks, font, background)

            # For all color write texts
            for color in self._color_reader.get_colors():

                # Get images by color
                for img in self.iterator_by_images(key=color.to_tuple(), images=images):

                    # Write all texts to image
                    for text_block in text_blocks_for_write:
                        # Write all texts
                        self._text_to_image_write_algorithm.write_text_to_image(
                            img=img.img,
                            text=text_block.rectangle.text,
                            font=img.font,
                            color=img.color,
                            x=text_block.x_left,
                            y=text_block.y_top,
                            image_name=img.filename
                        )

                    img = self.image_post_process(img)
                    self.save_image(img)
                    index += 1
                    if verbose:
                        print(f'Save new IMAGE: {index}:{img.filename}')
                    del img
