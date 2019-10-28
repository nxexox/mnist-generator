"""
Base classes for augmentations.

"""
import abc

from dataclasses import dataclass
from PIL import Image


@dataclass
class AugmentationFigure(abc.ABC):
    """
    Base class for Augmentation figure.

    """
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    border: int

    @classmethod
    @abc.abstractmethod
    def generate_random_figure(cls, w: int, h: int, max_linethickness: int, **kwargs) -> 'AugmentationFigure':
        """
        Generate Random Figure.

        :param int w: Holst width
        :param int h: Holst height
        :param int max_linethickness: Max line border

        :return: Random figure.
        :rtype: AugmentationFigure

        """
        pass


class DrawObject(abc.ABC):
    """
    Object for draw.

    """
    @abc.abstractmethod
    def draw(self, img: Image.Image) -> Image.Image:
        """
        Draw figure to image.

        :param Image.Image img: Image for draw

        :return: Drawing image
        :rtype: Image.Image

        """
        pass
