"""
Annotations writer.

"""
import abc
import os
from xml.etree import ElementTree as ETXml
from typing import List

from mnist_generator.storage import BaseStorage

from .annotation import BaseAnnotation, RegionPosition, Region, ImageAnnotation


class BaseAnnotationWriter(abc.ABC):
    """
    Base annotation writer class.

    """
    def write(self, annotation: BaseAnnotation, storage: BaseStorage, path: str):
        """
        Write annotation to file.

        :param BaseAnnotation annotation: Annotation object.
        :param BaseStorage storage: Storage object.
        :param str path: Path for write annotation.

        """
        pass


class AnnotationVOCPascalWriter(BaseAnnotationWriter):
    """
    Writer annotation for VOC Pascal format.

    """
    def _get_head(self, path: str) -> List[ETXml.Element]:
        """
        Get head document.

        :param str path: Path to file for create document.

        :return: Head document
        :rtype: List[ETXml.Element]

        <folder>folder</folder>
        <filename>example.jpg</filename>
        <size>
        <width>800</width>
        <height>600</height>
        <depth>3</depth>
        </size>

        """
        folder = ETXml.Element('folder')
        folder.text = os.path.basename(os.path.dirname(path))
        filename = ETXml.Element('filename')
        filename.text = os.path.basename(path)
        size = ETXml.Element('size')
        size_width = ETXml.SubElement(size, 'width')
        size_width.text = ''
        size_height = ETXml.SubElement(size, 'height')
        size_height.text = ''
        size_depth = ETXml.SubElement(size, 'depth')
        size_depth.text = ''

        return [folder, filename, size]

    def _get_annotations(self, name: str, position: RegionPosition) -> ETXml.Element:
        """
        Get annotation for text block.

        :param str name: Name text block
        :param RegionPosition position: Position text block.

        :return: Annotation text block element
        :rtype: ETXml.Element

        <object>
        <name>line</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <occluded>0</occluded>
        <difficult>0</difficult>
        <bndbox>
        <xmin>301</xmin>
        <ymin>85</ymin>
        <xmax>500</xmax>
        <ymax>124</ymax>
        </bndbox>
        </object>

        """
        obj = ETXml.Element('object')
        _name = ETXml.SubElement(obj, 'name')
        _name.text = name
        pose = ETXml.SubElement(obj, 'pose')
        pose.text = 'Unspecified'
        truncated = ETXml.SubElement(obj, 'truncated')
        truncated.text = '0'
        occluded = ETXml.SubElement(obj, 'occluded')
        occluded.text = '0'
        difficult = ETXml.SubElement(obj, 'difficult')
        difficult.text = '0'

        bndbox = ETXml.SubElement(obj, 'bndbox')
        xmin = ETXml.SubElement(bndbox, 'xmin')
        xmin.text = str(position.x_left)
        ymin = ETXml.SubElement(bndbox, 'ymin')
        ymin.text = str(position.y_top)
        xmax = ETXml.SubElement(bndbox, 'xmax')
        xmax.text = str(position.x_right)
        ymax = ETXml.SubElement(bndbox, 'ymax')
        ymax.text = str(position.y_bottom)

        return obj

    def _get_char_annotations(self, regions: List[Region]) -> List[ETXml.Element]:
        """
        Get char annotations.

        :param List[Region] regions: Annotation object

        :return: List element annotation objects
        :rtype: List[ETXml.Element]

        """
        return [
            self._get_annotations(name='symbol', position=region.position)
            for region in regions
        ]

    def _get_word_annotations(self, regions: List[Region]) -> List[ETXml.Element]:
        """
        Get word annotations.

        :param List[Region] regions: Annotation object

        :return: List element annotation objects
        :rtype: List[ETXml.Element]

        """
        return [
            self._get_annotations(name='word', position=region.position)
            for region in regions
        ]

    def _get_sentences_annotations(self, regions: List[Region]) -> List[ETXml.Element]:
        """
        Get sentence annotations.

        :param List[Region] regions: Annotation object

        :return: List element annotation objects
        :rtype: List[ETXml.Element]

        """
        return [
            self._get_annotations(name='line', position=region.position)
            for region in regions
        ]

    def _get_paragraph_annotations(self, regions: List[Region]) -> List[ETXml.Element]:
        """
        Get paragraph annotations.

        :param List[Region] regions: Annotation object

        :return: List element annotation objects
        :rtype: List[ETXml.Element]

        """
        return [
            self._get_annotations(name='paragraph', position=region.position)
            for region in regions
        ]

    def _get_text_block_annotations(self, regions: List[Region]) -> List[ETXml.Element]:
        """
        Get text blocks annotations.

        :param List[Region] regions: Annotation object

        :return: List element annotation objects
        :rtype: List[ETXml.Element]

        """
        return [
            self._get_annotations(name='artikle', position=region.position)
            for region in regions
        ]

    def _get_full_annotation(self, image_name: str, image_annotation: ImageAnnotation) -> ETXml.Element:
        """
        Get full annotation.

        :param str image_name: Image name.
        :param ImageAnnotation image_annotation: Image annotation.

        :return: Full Annotation element
        :rtype: ImageAnnotation

        """
        base = ETXml.Element('annotation')
        for el in self._get_head(image_name):
            base.append(el)

        for el in self._get_char_annotations(image_annotation.char_regions):
            base.append(el)

        for el in self._get_word_annotations(image_annotation.word_regions):
            base.append(el)

        for el in self._get_sentences_annotations(image_annotation.sentences_regions):
            base.append(el)

        for el in self._get_paragraph_annotations(image_annotation.paragraphs_regions):
            base.append(el)

        for el in self._get_text_block_annotations(image_annotation.texts_regions):
            base.append(el)

        return base

    def write(self, annotation: BaseAnnotation, storage: BaseStorage, path: str, verbose: bool = False):
        """
        Write annotation to files.

        :param BaseAnnotation annotation: Annotation object.
        :param BaseStorage storage: Storage object.
        :param str path: Path for write annotation.
        :param bool verbose: Verbose print progress?

        """
        for image_name, image_annotation in annotation.images.items():
            full_path = os.path.join(path, image_name)
            obj = self._get_full_annotation(os.path.join(path, image_name), image_annotation)
            str_obj = ETXml.tostring(obj)
            storage.write('{}.xml'.format(full_path), str_obj)
            if verbose:
                print(f'Save annotation {full_path}')
