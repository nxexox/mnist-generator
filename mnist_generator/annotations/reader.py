"""
Annotations reader.

"""
import abc
import os
from xml.dom import minidom
from typing import Iterable
from typing import Optional

from mnist_generator.storage import BaseStorage

from .annotation import ImageAnnotation, Region, RegionPosition


class BaseAnnotationReader(abc.ABC):
    """
    Base annotation reader class.

    """
    def __init__(self, path_to_folder: str, storage: BaseStorage):
        """
        Base annotation reader class.

        :param str path_to_folder: Path to folder in storage.
        :param BaseStorage storage: Storage for read annotations.

        """
        self.storage = storage
        self.path_to_folder = path_to_folder

    def read_all_files(self) -> Iterable[ImageAnnotation]:
        """
        Read all annotation files from storage.

        :return:

        """
        for file_path in self.storage.list(self.path_to_folder):
            yield self.read(file_path)

    @abc.abstractmethod
    def read(self, path_to_file: str, storage: Optional[BaseStorage] = None) -> ImageAnnotation:
        """
        Read annotations.

        :param str path_to_file: Path to file
        :param Optional[BaseStorage] storage: Storage for read

        :return: Image annotations
        :rtype: ImageAnnotation

        """
        pass


class VOCPascalAnnotationReader(BaseAnnotationReader):
    """
    VOC Pascal annotation reader class.

    """
    _mask_annotation = {
        'symbol': 'char_regions',
        'word': 'word_regions',
        'line': 'sentences_regions',
        'paragraph': 'paragraphs_regions',
        'artikle': 'texts_regions'
    }

    def read(self, path_to_file: str, storage: Optional[BaseStorage] = None) -> ImageAnnotation:
        """
        Read annotations.

        :param str path_to_file: Path to file
        :param Optional[BaseStorage] storage: Storage for read

        :return: Image annotations
        :rtype: ImageAnnotation

        """
        storage = storage or self.storage
        source_data = storage.read(path_to_file)
        return self.parse_document(source_data)

    def parse_document(self, source_data: str) -> ImageAnnotation:
        """
        Parse document from string.

        :param str source_data: Source data

        :return: Annotation object
        :rtype: ImageAnnotation

        """
        xml_doc = minidom.parseString(source_data)
        filename = xml_doc.getElementsByTagName('filename')[0].firstChild.nodeValue
        annotation = ImageAnnotation(file_name=filename)

        for obj in xml_doc.getElementsByTagName('object'):
            obj_type = obj.getElementsByTagName('name')[0].firstChild.nodeValue
            x_min = int(obj.getElementsByTagName('xmin')[0].firstChild.nodeValue)
            y_min = int(obj.getElementsByTagName('ymin')[0].firstChild.nodeValue)
            x_max = int(obj.getElementsByTagName('xmax')[0].firstChild.nodeValue)
            y_max = int(obj.getElementsByTagName('ymax')[0].firstChild.nodeValue)
            region = Region(
                position=RegionPosition(
                    x_left=x_min, y_top=y_min, x_right=x_max, y_bottom=y_max
                )
            )
            getattr(annotation, self._mask_annotation[obj_type]).append(region)

        return annotation
