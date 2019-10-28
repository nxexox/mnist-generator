"""
Compress for augmentation.

"""
import random

from PIL import Image

from .base import AugmentationFigure, DrawObject


class CompressObject(AugmentationFigure, DrawObject):
    """
    Compress object.

    """
    @classmethod
    def generate_random_figure(cls, w: int, h: int, **kwargs) -> 'CompressObject':
        """
        Generate Random Compress.

        :param int w: Holst width
        :param int h: Holst height

        :return: Random compress.
        :rtype: CompressObject

        """

        return cls(
            x_min=random.randint(1, w),
            y_min=random.randint(1, h),
            x_max=w, y_max=h,
            border=1
        )

    def draw(self, img: Image.Image) -> Image.Image:
        """
        Draw figure to image.

        :param Image.Image img: Image for draw

        """
        new_img = img.resize((self.x_max - self.x_min, self.y_max - self.y_min), Image.ANTIALIAS)
        new_img.format = img.format
        return new_img
