"""
Restore regions on image.

"""
from mnist_generator.annotations import BaseAnnotationReader
from mnist_generator.background import AbstractBackgrounds
from mnist_generator.image import ImageToIoBytesWriter

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

    def run(self):
        # TODO:
        pass
