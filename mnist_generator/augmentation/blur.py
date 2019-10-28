"""
Blur for augmentation.

"""
import random
import math

from PIL import Image, ImageFilter as PILImageFilter

from .base import AugmentationFigure, DrawObject


class BlurObject(AugmentationFigure, DrawObject):
    """
    Blur object.

    """
    @classmethod
    def generate_random_figure(cls, **kwargs) -> 'BlurObject':
        """
        Generate Random Blur.

        :return: Random figure.
        :rtype: BlurObject

        """
        return cls(1, 1, 1, 1, 1)

    def draw(self, img: Image.Image) -> Image.Image:
        """
        Draw figure to image.

        :param Image.Image img: Image for draw

        :return: Drawing image
        :rtype: Image.Image

        """
        filter_img = img.filter(
            PILImageFilter.GaussianBlur(radius=random.randint(1, 3))
        )
        filter_img = filter_img.convert('RGBA')
        filter_img.format = img.format
        return filter_img
