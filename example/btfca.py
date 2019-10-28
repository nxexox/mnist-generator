"""
Application.

"""
import os


from mnist_generator.storage import LocalStorage, FileReader
from mnist_generator.background import Backgrounds
from mnist_generator.colors import ColorsReader
from mnist_generator.fonts import FontsReader
from mnist_generator.image import TextToImageWriter, ImageToIoBytesWriter
from mnist_generator.annotations import Annotation, AnnotationVOCPascalWriter
from mnist_generator.texts import (
    TEXT_PARSER_WORDS_MODE, TEXT_PARSER_CHAR_MODE
)
from mnist_generator.algorithms import BTFCA
from mnist_generator.algorithms.packaging import BricksPackingAlgorithm


FONT_SIZE_RANGE = (30, 35)
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULT_DIR = os.path.join(DATA_DIR, 'result', 'images')
ANNOTATION_DIR = os.path.join(DATA_DIR, 'result', 'annotations')
print('PWD: {}, DATA_DIR: {}'.format(BASE_DIR, DATA_DIR))


storage = LocalStorage()
backgrounds = Backgrounds(path=os.path.join(DATA_DIR, 'backgrounds'), storage=storage)
text_reader = FileReader(path=os.path.join(DATA_DIR, 'texts'), storage=storage, file_mode='r')
color_reader = ColorsReader(path=os.path.join(DATA_DIR, 'colors.txt'), storage=storage)
font_reader = FontsReader(path=os.path.join(DATA_DIR, 'fonts'), storage=storage)
image_saver = ImageToIoBytesWriter(path=RESULT_DIR, storage=storage)
annotation = Annotation(region_modes=[TEXT_PARSER_CHAR_MODE])
text_to_image = TextToImageWriter(annotation=annotation)
bricks_algorithm = BricksPackingAlgorithm()


def run_btfca():
    algorithm = BTFCA(
        background_reader=backgrounds,
        text_reader=text_reader,
        fonts_reader=font_reader,
        color_reader=color_reader,
        image_saver=image_saver,
        font_size_range=FONT_SIZE_RANGE,
        packing_algorithm=bricks_algorithm,
        text_to_image_write_algorithm=text_to_image,
        parse_mode=TEXT_PARSER_WORDS_MODE,
        aug_degreeofrotation=1,
        aug_linethickness=1,
        aug_numberofoptions=1,
        aug_diameter=400,
        aug_amountpoints=1,
        augmentation_to_text=True
    )
    algorithm.run()


if __name__ == '__main__':
    run_btfca()
    annotation_writer = AnnotationVOCPascalWriter()
    annotation_writer.write(annotation, storage, ANNOTATION_DIR)
