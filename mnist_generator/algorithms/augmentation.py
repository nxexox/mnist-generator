import random
import math
import itertools
from typing import Tuple, Generator, List, Optional

from PIL import Image

from mnist_generator.augmentation import (
    AugmentationFigure,
    AugmentationFigureLine, AugmentationFigureEllipse, AugmentationFigureRectangle,
    AugmentationFigurePoint, DrawObject, GlareObject, BlurObject, CompressObject
)


class ImageAugmentation(object):
    """
    Image augmentation.

    """
    AUG_ROTATE = 'rotate'  # For text
    AUG_NEW_ELEMENTS = 'new_elements'
    AUG_GLARE = 'glare'  # Блики
    AUG_DEFOCUS = 'defocus'
    AUG_COMPRESSION = 'compression'  # Сжатие растяжение

    # Collections for augmentations
    rotate: List[DrawObject]
    new_elements: List[DrawObject]
    glare: List[DrawObject]
    defocus: List[DrawObject]
    compression: List[DrawObject]

    AUGS: Tuple[str] = (
        # AUG_ROTATE,
        AUG_NEW_ELEMENTS,
        # AUG_GLARE,
        AUG_DEFOCUS,
        AUG_COMPRESSION,
    )
    ELEMENTS: Tuple[AugmentationFigure] = (
        AugmentationFigureLine,
        AugmentationFigureEllipse, AugmentationFigureRectangle
    )

    def __init__(self, src_image: Image.Image,
                 aug_degreeofrotation: int, aug_linethickness: int, aug_numberofoptions: int,
                 aug_diameter: int, aug_amountpoints: int):
        """

        :param Image.Image src_image: Source Image for create augmentations.
        :param int aug_linethickness: Thickness Augmentation Patterns
        :param int aug_diameter: The diameter and diagonal of the other and the rectangles
        :param int aug_amountpoints: Count points

        aug_degreeofrotation - максимальный градус поворота текста
        aug_linethickness - максимальная ширина линии в пикселях для дополнительных элементов на изображении
        aug_numberofoptions - количество вариантов применения аугментации
        aug_diameter - диаметр кругов и диагональ прямоугольников
        aug_amountpoints - количество точек

        """
        self._src_image = src_image
        self._aug_numberofoptions = aug_numberofoptions  # Count augmentations
        self._aug_degreeofrotation = aug_degreeofrotation
        self._aug_linethickness = aug_linethickness
        self._aug_diameter = aug_diameter
        self._aug_amountpoints = aug_amountpoints

        for aug in self.AUGS:
            setattr(self, aug, list())

        self.standard_count = 0
        self.combinations_count = 0
        self.all_count = 0

    def copied_image(self) -> Image.Image:
        """
        :return: Copied image
        :rtype: Image.Image

        """
        img = self._src_image.copy()
        # if img.mode != 'RGBA':
        #     img = img.convert('RGBA')
        img.format = self._src_image.format
        return img

    def _calculate_new_elements(self) -> List[AugmentationFigure]:
        """
        Calculate figures for image.

        :return: List figures
        :rtype: List[AugmentationFigure]

        """
        return [
            random.choice(self.ELEMENTS).generate_random_figure(
                *self._src_image.size,
                max_linethickness=self._aug_linethickness,
                max_diameter=self._aug_diameter
            )
            for _ in range(self._aug_numberofoptions)
        ] + [
            AugmentationFigurePoint.generate_random_figure(
                *self._src_image.size,
                max_linethickness=self._aug_linethickness,
                max_diameter=self._aug_diameter
            )
            for _ in range(self._aug_amountpoints)
        ]

    def _calculate_rotate(self) -> List[DrawObject]:
        return []

    def _calculate_glare(self) -> List[DrawObject]:
        """
        Create glare for image.

        :return: List[DrawObject]

        """
        return [
            GlareObject.generate_random_figure(*self._src_image.size)
            for _ in range(self._aug_numberofoptions)
        ]

    def _calculate_defocus(self) -> List[DrawObject]:
        """
        Create blur to image.

        :return: List blurs
        :rtype: List[DrawObject]

        """
        return [BlurObject.generate_random_figure()]

    def _calculate_compression(self) -> List[DrawObject]:
        """
        Create compress from image.

        :return: List compress operations
        :rtype: List[DrawObject]

        """
        return [
            CompressObject.generate_random_figure(*self._src_image.size)
            for _ in range(self._aug_numberofoptions)
        ]

    def calculate_all_variants(self) -> int:
        """
        Calculate all variants.

        :return: Count all variants
        :rtype: int

        """
        self.standard_count = 0
        for aug in self.AUGS:
            handler = getattr(self, '_calculate_{}'.format(aug))
            setattr(self, aug, handler())
            self.standard_count += len(getattr(self, aug))

        def C(n: int, k: int) -> int:
            return int(math.factorial(n) / (math.factorial(k) * math.factorial(n - k)))

        for i in range(self.standard_count):
            self.combinations_count += C(self.standard_count, i)

        self.all_count = self.standard_count + self.combinations_count

        return self.all_count

    def draw_to_image(self, obj: DrawObject, img: Optional[Image.Image] = None) -> Image.Image:
        """
        Draw to image.

        :param DrawObject obj: Draw object for write to image.
        :param Optional[Image.Image] img: Image for draw

        :return: Image
        :rtype: Image.Image

        """
        img = img or self.copied_image()
        img = obj.draw(img)
        return img

    def get_iterator_by_all_elements(self) -> Generator[DrawObject, None, None]:
        """
        Iterator by all elements in collections.

        :return: Iterator DrawObjects
        :rtype: Image.Image

        """
        for draw in itertools.chain(*(getattr(self, aug) for aug in self.AUGS)):
            yield draw

    def get_iterator_by_combinations(self) -> Generator[List[DrawObject], None, None]:
        """
        Iterator by all combinations elements.

        :return: Iterator by all combinations
        :rtype: Generator[List[Image.Image], None, None]

        """
        all_augmentations = [getattr(self, aug) for aug in self.AUGS]
        for i in range(1, self.all_count):
            for draws in itertools.combinations(itertools.chain(*all_augmentations), i):
                yield draws

    def draws(self) -> Generator[Image.Image, None, None]:
        """
        Draws all augmentations by image.

        :return: Generator augmentation images
        :rtype: Generator[Image.Image, None, None]

        """
        for augmentation in self.get_iterator_by_all_elements():
            _img = self.draw_to_image(augmentation)
            yield _img

        for augmentations in self.get_iterator_by_combinations():
            img = self.copied_image()
            for aug in augmentations:
                img = self.draw_to_image(aug, img)
            yield img
