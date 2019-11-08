# MNIST Generator by Python

Генератор изображений с текстом, аугментацией и прочим.

## Какие есть алгоритмы?

* `BTFC` - Перебираем все фоны, для каждого фона все тексты, для каждого текста все шрифты, для каждого шрифта все размеры шрифтов, для каждого размера все цвета.

Изображения, тексты, шрифты, цвета необходимо подготовить заранее.

* `BTFCA` - Это как `BTFC`, только для каждого готового изображения добавляются несоклько вариаций с аугментацией фона.
Параметры аугментации регулируются отдельно.

* `RestoreRegionsByAnnotation` -  Восстановление регионов по файлам аннотации. Создает изобаржения с подсвеченными регионами.

## Пример (Больше примеров в папке example):

```python
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


# Готовим данные для алгоритмов
FONT_SIZE_RANGE = (30, 35)
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULT_DIR = os.path.join(DATA_DIR, 'result', 'images')
ANNOTATION_DIR = os.path.join(DATA_DIR, 'result', 'annotations')
print('PWD: {}, DATA_DIR: {}'.format(BASE_DIR, DATA_DIR))


storage = LocalStorage()
# Инициализируем компоненты, для работы алгоритма BTFC.
# Такое множество компонентов необходимо, что бы с легкостью подменять любую часть алгоритма на свою
# Например подменить лоакальное хранилище на S3
btfc_backgrounds = Backgrounds(path=os.path.join(DATA_DIR, 'backgrounds'), storage=storage)
btfc_text_reader = FileReader(path=os.path.join(DATA_DIR, 'texts'), storage=storage, file_mode='r')
btfc_color_reader = ColorsReader(path=os.path.join(DATA_DIR, 'colors.txt'), storage=storage)
btfc_font_reader = FontsReader(path=os.path.join(DATA_DIR, 'fonts'), storage=storage)
btfc_image_saver = ImageToIoBytesWriter(path=RESULT_DIR, storage=storage)
btfc_annotation = Annotation(region_modes=[TEXT_PARSER_WORDS_MODE])
btfc_text_to_image = TextToImageWriter(annotation=annotation)
btfc_bricks_algorithm = BricksPackingAlgorithm()  # Алгоритм расположения текста на изображении

# Инициализируем компоненты для алгоритма восстановления регионов.
restore_image_reader = Backgrounds(path=RESULT_DIR, storage=storage)
restore_image_saver = ImageToIoBytesWriter(path=os.path.join(DATA_DIR, 'result', 'restore'), storage=storage)
restore_annotation_reader = VOCPascalAnnotationReader(path_to_folder=ANNOTATION_DIR, storage=storage)


def run_btfc():
    print('INIT BTFC')
    algorithm = BTFC(
        background_reader=btfc_backgrounds,
        text_reader=btfc_text_reader,
        fonts_reader=btfc_font_reader,
        color_reader=btfc_color_reader,
        image_saver=btfc_image_saver,
        font_size_range=FONT_SIZE_RANGE,
        packing_algorithm=btfc_bricks_algorithm,
        text_to_image_write_algorithm=btfc_text_to_image,
        parse_mode=TEXT_PARSER_WORDS_MODE
    )
    print('RUN BTFC')
    algorithm.run(verbose=True)
    print('END BTFC')
    print('RUN WRITE ANNOTATION')
    annotation_writer = AnnotationVOCPascalWriter()
    annotation_writer.write(btfc_annotation, storage, ANNOTATION_DIR, verbose=True)
    print('END WRITE ANNOTATION')


def run_restore():
    print('INIT RESTORE')
    algorithm = RestoreRegionsByAnnotation(
        image_reader=restore_image_reader,
        image_writer=restore_image_saver,
        annotation_reader=restore_annotation_reader
    )
    print('RUN RESTORE')
    algorithm.run(verbose=True)
    print('END RESTORE')


if __name__ == '__main__':
    run_btfc()
    run_restore()
```

# TODO:
* Описать все компоненты системы
* Добавить документацию по различным кейсам использования
* Добавить алгоритмов упаковки текста на картинке
* Добавить setup.py и тесты
* Добавить быстрые скрипты в либу
