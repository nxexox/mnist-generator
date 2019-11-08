"""
Application.

"""
import os


from mnist_generator.storage import LocalStorage, FileReader
from mnist_generator.background import Backgrounds
from mnist_generator.colors import ColorsReader
from mnist_generator.fonts import FontsReader
from mnist_generator.image import TextToImageWriter, ImageToIoBytesWriter
from mnist_generator.annotations import Annotation, AnnotationVOCPascalWriter, VOCPascalAnnotationReader
from mnist_generator.texts import (
    TEXT_PARSER_WORDS_MODE, TEXT_PARSER_CHAR_MODE
)
from mnist_generator.algorithms import BTFC, RestoreRegionsByAnnotation
from mnist_generator.algorithms.packaging import BricksPackingAlgorithm


FONT_SIZE_RANGE = (30, 35)
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULT_DIR = os.path.join(DATA_DIR, 'result', 'images')
ANNOTATION_DIR = os.path.join(DATA_DIR, 'result', 'annotations')
print('PWD: {}, DATA_DIR: {}'.format(BASE_DIR, DATA_DIR))


storage = LocalStorage()
# For BTFC
backgrounds = Backgrounds(path=os.path.join(DATA_DIR, 'backgrounds'), storage=storage)
text_reader = FileReader(path=os.path.join(DATA_DIR, 'texts'), storage=storage, file_mode='r')
color_reader = ColorsReader(path=os.path.join(DATA_DIR, 'colors.txt'), storage=storage)
font_reader = FontsReader(path=os.path.join(DATA_DIR, 'fonts'), storage=storage)
image_saver = ImageToIoBytesWriter(path=RESULT_DIR, storage=storage)
annotation = Annotation(region_modes=[TEXT_PARSER_WORDS_MODE])
text_to_image = TextToImageWriter(annotation=annotation)
bricks_algorithm = BricksPackingAlgorithm()
# For Restore
image_reader = Backgrounds(path=RESULT_DIR, storage=storage)
restore_image_saver = ImageToIoBytesWriter(path=os.path.join(DATA_DIR, 'result', 'restore'), storage=storage)
annotation_reader = VOCPascalAnnotationReader(path_to_folder=ANNOTATION_DIR, storage=storage)


def run_btfc():
    print('INIT BTFC')
    algorithm = BTFC(
        background_reader=backgrounds,
        text_reader=text_reader,
        fonts_reader=font_reader,
        color_reader=color_reader,
        image_saver=image_saver,
        font_size_range=FONT_SIZE_RANGE,
        packing_algorithm=bricks_algorithm,
        text_to_image_write_algorithm=text_to_image,
        parse_mode=TEXT_PARSER_WORDS_MODE
    )
    print('RUN BTFC')
    algorithm.run(verbose=True)
    print('END BTFC')
    print('RUN WRITE ANNOTATION')
    annotation_writer = AnnotationVOCPascalWriter()
    annotation_writer.write(annotation, storage, ANNOTATION_DIR, verbose=True)
    print('END WRITE ANNOTATION')


def run_restore():
    print('INIT RESTORE')
    algorithm = RestoreRegionsByAnnotation(
        image_reader=image_reader, image_writer=restore_image_saver,
        annotation_reader=annotation_reader
    )
    print('RUN RESTORE')
    algorithm.run(verbose=True)
    print('END RESTORE')


if __name__ == '__main__':
    run_btfc()
    run_restore()
