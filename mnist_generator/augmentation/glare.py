"""
Glare for augmentation.

"""
import random
import math

from PIL import Image, ImageDraw as PILImageDraw

from .base import AugmentationFigure, DrawObject


class GlareObject(AugmentationFigure, DrawObject):
    """
    Glare object.

    """
    @classmethod
    def generate_random_figure(cls, w: int, h: int, **kwargs) -> 'GlareObject':
        """
        Generate Random Figure.

        :param int w: Holst width
        :param int h: Holst height

        :return: Random figure.
        :rtype: GlareObject

        """
        diameter = random.randint(1, max((w, h)) / 4)
        x_min = random.randint(0, w)
        y_min = x_min

        # Calculate x_max, y_max
        indent = diameter * math.cos(45)
        x_max, y_max = x_min + indent, y_min + indent
        return cls(
            x_min=int(x_min), y_min=int(x_min),
            x_max=int(x_max), y_max=int(x_max),
            border=1
        )

    def draw(self, img: Image.Image) -> Image.Image:
        """
        Draw figure to image.

        :param Image.Image img: Image for draw

        :return: Drawing image
        :rtype: Image.Image

        """
        draw = PILImageDraw.Draw(img, 'RGBA')
        draw.ellipse((self.x_min, self.y_min, self.x_max, self.y_max), fill=(255, 255, 255, 125))
        return img
