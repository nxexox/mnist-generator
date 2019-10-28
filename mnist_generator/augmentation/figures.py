"""
Figures for draw to image.

"""
import random
import math

from PIL import ImageDraw as PILImageDraw, Image
from dataclasses import dataclass

from .base import AugmentationFigure, DrawObject


@dataclass
class AugmentationFigurePoint(AugmentationFigure, DrawObject):
    """
    Augmentation Point figure.

    """
    @classmethod
    def generate_random_figure(cls, w: int, h: int, max_linethickness: int, **kwargs) -> 'AugmentationFigure':
        """
        Generate Random Figure.

        :param int w: Holst width
        :param int h: Holst height
        :param int max_linethickness: Max line border

        :return: Random figure.
        :rtype: AugmentationFigure

        """
        x_min = random.randint(0, w)
        y_min = random.randint(0, h)
        return cls(
            x_min=x_min, y_min=y_min,
            x_max=x_min, y_max=y_min,
            border=1
        )

    def draw(self, img: Image.Image) -> Image.Image:
        """
        Draw figure to image.

        :param Image.Image img: Image for draw

        :return: Drawing image
        :rtype: Image.Image

        """
        draw = PILImageDraw.Draw(img)
        draw.point((self.x_min, self.y_min), fill=(255, 255, 255))
        return img


@dataclass
class AugmentationFigureLine(AugmentationFigure, DrawObject):
    """
    Augmentation Line figure.

    """
    @classmethod
    def generate_random_figure(cls, w: int, h: int, max_linethickness: int, **kwargs) -> 'AugmentationFigure':
        """
        Generate Random Figure.

        :param int w: Holst width
        :param int h: Holst height
        :param int max_linethickness: Max line border

        :return: Random figure.
        :rtype: AugmentationFigure

        """
        x_min, y_min = random.randint(0, w), random.randint(0, h)
        return cls(
            x_min=x_min, y_min=y_min,
            x_max=random.randint(x_min, w),
            y_max=random.randint(y_min, h),
            border=random.randint(1, max_linethickness)
        )

    def draw(self, img: Image.Image) -> Image.Image:
        """
        Draw figure to image.

        :param Image.Image img: Image for draw

        :return: Drawing image
        :rtype: Image.Image

        """
        draw = PILImageDraw.Draw(img)
        draw.line((self.x_min, self.y_min, self.x_max, self.y_max), fill=(255, 255, 255), width=self.border)
        return img


@dataclass
class AugmentationFigureEllipse(AugmentationFigure, DrawObject):
    """
    Augmentation Ellipse figure.

    """
    @classmethod
    def generate_random_figure(cls, w: int, h: int, max_linethickness: int, max_diameter: int,
                               **kwargs) -> 'AugmentationFigure':
        """
        Generate Random Figure.

        :param int w: Holst width
        :param int h: Holst height
        :param int max_linethickness: Max line border
        :param int max_diameter: Max figure diameter

        :return: Random figure.
        :rtype: AugmentationFigure

        """
        diameter = random.randint(1, max_diameter)
        x_min = random.randint(0, w)
        y_min = x_min

        # Calculate x_max, y_max
        indent = diameter * math.cos(45)
        x_max, y_max = x_min + indent, y_min + indent
        return cls(
            x_min=int(x_min), y_min=int(x_min),
            x_max=int(x_max), y_max=int(x_max),
            border=random.randint(1, max_linethickness)
        )

    def draw(self, img: Image.Image) -> Image.Image:
        """
        Draw figure to image.

        :param Image.Image img: Image for draw

        :return: Drawing image
        :rtype: Image.Image

        """
        draw = PILImageDraw.Draw(img)
        draw.ellipse((self.x_min, self.y_min, self.x_max, self.y_max), fill=None, outline=(255, 255, 255))
        return img


@dataclass
class AugmentationFigureRectangle(AugmentationFigure, DrawObject):
    """
    Augmentation Rectangle figure.

    """
    @classmethod
    def generate_random_figure(cls, w: int, h: int, max_linethickness: int, max_diameter: int,
                               **kwargs) -> 'AugmentationFigure':
        """
        Generate Random Figure.

        :param int w: Holst width
        :param int h: Holst height
        :param int max_linethickness: Max line border
        :param int max_diameter: Max figure diameter

        :return: Random figure.
        :rtype: AugmentationFigure

        """
        diameter = random.randint(1, max_diameter)
        x_min = random.randint(0, w)
        y_min = random.randint(0, h)
        indent = diameter / random.randint(2, 5)
        x_max = x_min + indent
        y_max = y_min + (diameter - indent)

        return cls(
            x_min=int(x_min), y_min=int(y_min),
            x_max=int(x_max), y_max=int(y_max),
            border=random.randint(1, max_linethickness)
        )

    def draw(self, img: Image.Image) -> Image.Image:
        """
        Draw figure to image.

        :param Image.Image img: Image for draw

        :return: Drawing image
        :rtype: Image.Image

        """
        draw = PILImageDraw.Draw(img)
        draw.rectangle((self.x_min, self.y_min, self.x_max, self.y_max), fill=None, outline=(255, 255, 255), width=self.border)
        return img
