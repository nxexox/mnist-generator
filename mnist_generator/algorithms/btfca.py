"""
Algorithm for full iteration:
 -> Backgrounds
 -> Texts
 -> Fonts and fonts sized
 -> Colors
 -> Augmentations

"""
from typing import Tuple, Generator, Union, List, Dict, Any

from PIL import Image

from mnist_generator.fonts import Font

from .augmentation import ImageAugmentation
from .btfc import BTFC, BTFCImage


class BTFCA(BTFC):
    """
    Algorithm for full iteration:
     -> Backgrounds
     -> Texts
     -> Fonts and fonts sized
     -> Colors
     -> Augmentations

    """
    def __init__(self, aug_degreeofrotation: int, aug_linethickness: int, aug_numberofoptions: int,
                 aug_diameter: int, aug_amountpoints: int, augmentation_to_text: bool = False, *args, **kwargs):
        """
        Algorithm for full iteration:
         -> Backgrounds
         -> Texts
         -> Fonts and fonts sized
         -> Colors
         -> Augmentations

        :param int aug_degreeofrotation: Max text rotate
        :param int aug_linethickness: Thickness Augmentation Patterns
        :param int aug_numberofoptions: Count drw augmentation
        :param int aug_diameter: The diameter and diagonal of the other and the rectangles
        :param int aug_amountpoints: Count points
        :param bool augmentation_to_text: Augmentation after text?

        """
        super().__init__(*args, **kwargs)
        self._aug_numberofoptions = aug_numberofoptions  # Count augmentations
        self._aug_degreeofrotation = aug_degreeofrotation
        self._aug_linethickness = aug_linethickness
        self._aug_diameter = aug_diameter
        self._aug_amountpoints = aug_amountpoints
        self._augmentation_to_text = augmentation_to_text

    def get_base_images(self, background: Image.Image,
                        font: Font) -> Dict[Tuple[int, int, int], List[BTFCImage]]:
        """
        Get images for write.

        :param Image.Image background: Background
        :param Font font: Font for calculate.

        :return: Images dict for write.
        :rtype: Dict[Tuple[int, int, int], List[BTFCImage]]

        """
        # If augmentation before text to write
        if self._augmentation_to_text:
            return super().get_base_images(background, font)

        result = {}
        for color in self._color_reader.get_colors():
            augmentation = ImageAugmentation(
                src_image=self._get_image_for_write(background),
                aug_amountpoints=self._aug_amountpoints,
                aug_degreeofrotation=self._aug_degreeofrotation,
                aug_diameter=self._aug_diameter,
                aug_linethickness=self._aug_linethickness,
                aug_numberofoptions=self._aug_numberofoptions
            )

            augmentation.calculate_all_variants()

            key = color.to_tuple()
            result[key] = [
                BTFCImage(img=img, color=color, font=font, filename=self.get_result_file_name(background))
                for img in augmentation.draws()
            ]

        return result

    def iterator_by_images(self, key: Any,
                           images: Dict[Tuple[int, int, int], Union[List[BTFCImage], BTFCImage]]) \
            -> Generator[BTFCImage, None, None]:
        """
        Iterator by images.

        :param Any key: Key for get images
        :param Dict[Tuple[int, int, int], Union[List[BTFCImage], BTFCImage]] images: Images for get iterator

        :return: Generator[BTFCImage, None, None]

        """
        imgs = images[key]
        if isinstance(imgs, list):
            for img in imgs:
                yield img
        else:
            yield imgs

    def image_post_process(self, img: BTFCImage, index: int) -> BTFCImage:
        """
        Post processing image after save to storage.

        :param Image.Image img: Image for processing.
        :param int index: Current image index in global cycle.

        :return: Processing image
        :rtype: BTFCImage

        """
        if self._augmentation_to_text:
            augmentation = ImageAugmentation(
                src_image=self._get_image_for_write(img.img),
                aug_amountpoints=self._aug_amountpoints,
                aug_degreeofrotation=self._aug_degreeofrotation,
                aug_diameter=self._aug_diameter,
                aug_linethickness=self._aug_linethickness,
                aug_numberofoptions=self._aug_numberofoptions
            )
            augmentation.calculate_all_variants()
            for _img in augmentation.draws():
                btfc_img = BTFCImage(
                    img=_img,
                    color=img.color,
                    font=img.font,
                    filename=self.get_result_file_name(_img)
                )
                self.save_image(btfc_img, index)

        return img
