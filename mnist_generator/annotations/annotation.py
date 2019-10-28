"""
Annotation class.

"""
import abc
from typing import List, Tuple, Optional, Dict
from collections import defaultdict

from dataclasses import dataclass, field

from mnist_generator.texts import TextGeneratorParser, AbstractTextParser
from mnist_generator.fonts import Font


ANNOTATION_CHAR_MODE = 'chars'
ANNOTATION_WORDS_MODE = 'words'
ANNOTATION_SENTENCES_MODE = 'sentences'
ANNOTATION_PARAGRAPHS_MODE = 'paragraphs'
ANNOTATION_TEXT_BLOCKS_MODE = 'text'
ALLOWED_ANNOTATIONS_MODES = (
    ANNOTATION_CHAR_MODE, ANNOTATION_WORDS_MODE,
    ANNOTATION_SENTENCES_MODE, ANNOTATION_PARAGRAPHS_MODE,
    ANNOTATION_TEXT_BLOCKS_MODE
)


@dataclass
class RegionPosition(object):
    x_left: int
    y_top: int
    x_right: int
    y_bottom: int


@dataclass
class Region(object):
    position: RegionPosition
    text: Optional[str] = None


@dataclass
class ImageAnnotation(object):
    char_regions: List[Region] = field(default_factory=list)
    word_regions: List[Region] = field(default_factory=list)
    sentences_regions: List[Region] = field(default_factory=list)
    paragraphs_regions: List[Region] = field(default_factory=list)
    texts_regions: List[Region] = field(default_factory=list)


class BaseAnnotation(abc.ABC):
    """
    Base Annotation class.

    """
    text_parser_class = TextGeneratorParser
    _regions_map = {
        ANNOTATION_CHAR_MODE: 'char_regions',
        ANNOTATION_WORDS_MODE: 'word_regions',
        ANNOTATION_SENTENCES_MODE: 'sentences_regions',
        ANNOTATION_PARAGRAPHS_MODE: 'paragraphs_regions',
        ANNOTATION_TEXT_BLOCKS_MODE: 'texts_regions'
    }

    def __init__(self, region_modes: List[str], text_parser_class: Optional[AbstractTextParser] = None):
        """
        Base Annotation class.

        :param List[str] region_modes: Modes for save regions
        :param Optional[AbstractTextParser] text_parser_class: Class for text parser

        """
        if set(region_modes) - set(ALLOWED_ANNOTATIONS_MODES):
            raise ValueError(
                'The argument `region_modes` not valid value. Valid {}'.format(ANNOTATION_TEXT_BLOCKS_MODE)
            )
        # Normalizing regions
        self._region_modes = list(sorted(region_modes, key=lambda x: ALLOWED_ANNOTATIONS_MODES.index(x)))
        self.text_parser_class = text_parser_class or self.text_parser_class
        self._images = defaultdict(ImageAnnotation)

    @property
    def images(self) -> Dict[str, ImageAnnotation]:
        """
        :return: Annotations images.
        :rtype: Dict[str, ImageAnnotation]

        """
        return self._images

    @abc.abstractmethod
    def add_new_regions(self, image_name: str, region_text: str, x: int, y: int, font: Font):
        """
        Add new regions.

        :param str image_name: Image name for added region to image
        :param str region_text: Text for split by regions
        :param int x: Left x position to start regions
        :param int y: Top position to start regions
        :param Font font: Font for calculate text size

        """
        pass

    @abc.abstractmethod
    def add_new_region(self, image_name: str, region_text: str, region_position: RegionPosition, region_type: str):
        """
        Added region to image.

        :param str image_name: Image name for search image.
        :param str region_text: Text in region
        :param RegionPosition region_position: Region position for save.
        :param str region_type: Region type for current write.

        """
        pass


class Annotation(BaseAnnotation):
    """
    Annotation class.

    """
    def add_new_regions(self, image_name: str, region_text: str, x: int, y: int, font: Font):
        """
        Add new regions.

        :param str image_name: Image name for added region to image
        :param str region_text: Text for split by regions
        :param int x: Left x position to start regions
        :param int y: Top position to start regions
        :param Font font: Font for calculate text size

        """
        # TODO: Тут делае более умный алгоритм для нескольких типов блоков.
        # Идем от большего к меньшему по размеру блоков
        # Сначала просчитываем и записываем большой блок, потом для этого большого блока парсим на более детальные просчитываем и записываем их,
        # Потом след большой блок и т.д.
        for region_mode in reversed(self._region_modes):
            old_region = [x, y]
            full_region = font.font.getsize_multiline(region_text)
            index_for_char = 0
            for text_block in self.text_parser_class.get_text_blocks(text=region_text,
                                                                     mode=region_mode,
                                                                     added_separator=True):
                text_size = font.font.getsize_multiline(text_block)
                _x = old_region[0] + text_size[0]
                # TODO: It is supposed that one line gets to a method, without transfer
                # Y calculate UpperCase_bottom_position - text_block_size, If have upper case in string
                _y = old_region[1] + full_region[1]
                old_region[1] = _y - text_size[1]

                if region_mode != ANNOTATION_CHAR_MODE or index_for_char % 2 == 0:
                    self.add_new_region(
                        image_name=image_name, region_text=text_block,
                        region_position=RegionPosition(old_region[0], old_region[1], _x, _y),
                        region_type=region_mode
                    )

                old_region[0] = _x
                old_region[1] = y

    def add_new_region(self, image_name: str, region_text: str, region_position: RegionPosition, region_type: str):
        """
        Added region to image.

        :param str image_name: Image name for search image.
        :param str region_text: Text in region
        :param Tuple[int, int, int, int] region_position: Region position for save.
        :param str region_type: Region type for current write.

        """
        image_annotation = self._images[image_name]  # type: ImageAnnotation
        regions_array = getattr(image_annotation, self._regions_map[region_type])
        regions_array.append(Region(text=region_text, position=region_position))
