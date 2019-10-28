"""
Bricks easy algorithm.

"""
from typing import List

from .base import BasePackagingAlgorithm, Rectangle, RectanglePosition


class BricksPackingAlgorithm(BasePackagingAlgorithm):
    """
    Bricks easy algorithm.

    """
    def packing(self, holst: Rectangle, rectangles: List[Rectangle]) -> List[RectanglePosition]:
        """
        Bricks easy algorithm.

        :param Rectangle holst: Holst for calculate blocks.
        :param List[Rectangle] rectangles: List rectangles.

        :return: Array coordinats
        :rtype: List[RectanglePosition]

        """
        current_x_position = 0
        current_y_position = 0
        last_top_bottom = 0
        result = []

        for r in rectangles:
            if holst.w - current_x_position >= r.w:
                if holst.h - current_y_position >= r.h:
                    result.append(
                        RectanglePosition(
                            rectangle=r,
                            x_left=current_x_position,
                            y_top=current_y_position,
                            x_right=current_x_position + r.w,
                            y_bottom=current_y_position + r.h
                        )
                    )
                    last_top_bottom = max((last_top_bottom, current_y_position + r.h))
                    current_x_position += r.w
            elif holst.h - current_y_position >= r.h and holst.w - r.w >= 0:
                current_x_position = 0
                current_y_position = last_top_bottom
                result.append(
                    RectanglePosition(
                        rectangle=r,
                        x_left=current_x_position, y_top=current_y_position,
                        x_right=current_x_position + r.w, y_bottom=current_y_position + r.h
                    )
                )
                last_top_bottom = max((last_top_bottom, current_y_position + r.h))
                current_x_position += r.w

        return result
