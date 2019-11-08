"""
Restore regions on image.

"""
import os
from typing import List

from mnist_generator.annotations import (
    BaseAnnotationReader, ALLOWED_ANNOTATIONS_MODES,
    REGIONS_MAP, Region
)
from mnist_generator.background import AbstractBackgrounds
from mnist_generator.image import ImageToIoBytesWriter
from mnist_generator.augmentation import AugmentationFigureRectangle

from .base import BaseAlgorithm


class RestoreRegionsByAnnotation(BaseAlgorithm):
    """
    Restore regions by annotations.

    """
    def __init__(self, image_reader: AbstractBackgrounds, image_writer: ImageToIoBytesWriter,
                 annotation_reader: BaseAnnotationReader):
        """
        Restore regions by annotations.

        :param AbstractBackgrounds image_reader: Images reader.
        :param ImageToIoBytesWriter image_writer: Images writer
        :param BaseAnnotationReader annotation_reader: Annotations reader

        """
        self._image_reader = image_reader
        self._image_writer = image_writer
        self._annotation_reader = annotation_reader

    def run(self, verbose: bool = False):
        """
        Restore regions algorithm.

        :param bool verbose: Verbose debug messages?

        """
        index = 0

        for annotation in self._annotation_reader.read_all_files():
            src_img = self._image_reader.reader.read_file(
                os.path.join(self._image_reader.reader._path, annotation.file_name)
            )

            for annotation_type in ALLOWED_ANNOTATIONS_MODES:
                current_type_annotates = getattr(annotation, REGIONS_MAP[annotation_type])  # type: List[Region]

                for ant in current_type_annotates:
                    rectangle = AugmentationFigureRectangle(
                        x_min=ant.position.x_left,
                        x_max=ant.position.x_right,
                        y_min=ant.position.y_top,
                        y_max=ant.position.y_bottom,
                        border=3,
                        fill=None,
                        outline=(255, 0, 0)
                    )
                    src_img = rectangle.draw(src_img)

            self._image_writer.write(annotation.file_name, src_img)
            index += 1
            del src_img
            if verbose:
                print(f'Save restored image {index}:{annotation.file_name}')
