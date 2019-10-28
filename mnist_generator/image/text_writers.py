"""
Class Text to image writers.

"""
import abc
from typing import Optional

from PIL import ImageDraw as PilImageDraw, Image

from mnist_generator.texts import AbstractTextParser, TextGeneratorParser
from mnist_generator.fonts import Font
from mnist_generator.colors import Color
from mnist_generator.annotations import BaseAnnotation


class TextToImageWriter(abc.ABC):
    """
    Text to image writer.

    """
    text_parser_class = TextGeneratorParser

    def __init__(self, annotation: BaseAnnotation, text_parser_class: Optional[AbstractTextParser] = None):
        """
        Text to image writer.

        :param BaseAnnotation annotation: Annotation class for create annotation from write text.
        :param Optional[AbstractTextParser] text_parser_class: Text parser class.

        """
        self.annotation = annotation
        self.text_parser_class = text_parser_class or self.text_parser_class

    def write_text_to_image(self, img: Image, text: str, font: Font, color: Color, x: int, y: int, image_name: str):
        """
        Write text to image.

        :param PIL.Image.Image img: Image for write
        :param str text: Text for write
        :param Font font: Font object fot write to image
        :param Color color: Color for write text
        :param int x: Position start text
        :param int y: Position end text
        :param str image_name: Image name for annotation.

        """
        d = PilImageDraw.Draw(img)
        d.multiline_text((x, y), text, font=font.font, fill=color.to_tuple())

        # Calculate text region
        self.annotation.add_new_regions(image_name=image_name, region_text=text, x=x, y=y, font=font)
