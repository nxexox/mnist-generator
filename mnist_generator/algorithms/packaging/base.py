"""
Base class for Packaging algorithms.

"""
import abc
from typing import List, Tuple, Optional

from dataclasses import dataclass


@dataclass
class Rectangle(object):
    rectangle_id: str
    w: int
    h: int
    text: Optional[str] = None


@dataclass
class RectanglePosition(object):
    rectangle: Rectangle
    x_left: int
    y_top: int
    x_right: int
    y_bottom: int


class BasePackagingAlgorithm(abc.ABC):
    """
    Base packing algorithm

    """
    def create_holst(self, w: int, h: int) -> Rectangle:
        """
        Create holst for calculate.

        :param int w: Width
        :param int h: Height

        :return: Rectangle object
        :rtype: Rectangle

        """
        return Rectangle(rectangle_id='holst', w=w, h=h)

    def create_rectangles(self, rectangle: List[Tuple[int, int, Optional[str]]]) -> List[Rectangle]:
        """
        Create rectangles from src data.

        :param List[Tuple[int, int, Optional[str]] rectangle: List source rectangles

        :return: List[Rectangle]
        :rtype: List rectangle objects.

        """
        return [
            Rectangle(str(index), rectangle[0], rectangle[1], rectangle[2] if len(rectangle) > 2 else None)
            for index, rectangle in enumerate(rectangle)
        ]

    @abc.abstractmethod
    def packing(self, holst: Rectangle, rectangles: List[Rectangle]) -> List[RectanglePosition]:
        """
        Packing method.

        :param Rectangle holst: Holst for calculate blocks.
        :param List[Rectangle] rectangles: List rectangles.

        :return: Array coordinats
        :rtype: List[RectanglePosition]

        """
        pass
