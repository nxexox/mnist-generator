import abc
import mimetypes
from typing import Generator

from PIL import Image

from mnist_generator.storage import BaseStorage, LocalStorage, BaseFileChecker, FileReader, FileWriter


class ImageFileChecker(BaseFileChecker):
    """
    Checker for images.

    """
    def ignore(self, file_path: str) -> bool:
        """
        Ignore file?

        :param str file_path: Path to file.

        :return: Result check
        :rtype: bool

        """
        mt = mimetypes.guess_type(file_path)[0]
        mt = mt.split('/')[0] if mt else mt
        return mt != 'image'


class ImageReader(FileReader):
    """
    Images reader.

    """
    storage = LocalStorage()
    file_checker = ImageFileChecker()

    def images_from_storage_generator(self) -> Generator[Image.Image, None, None]:
        """
        Generator for images from storage.

        :return: Image files generator
        :rtype: Generator[Image.Image, None, None]

        """
        for file_path in self.get_files_patches_from_storage():
            yield Image.open(file_path)


class AbstractBackgrounds(abc.ABC):
    """
    Base abstract backgrounds.

    """
    writer_class = None  # type: type(FileWriter)
    reader_class = None  # type: type(FileReader)
    _reader = None  # type: ImageReader
    _writer = None  # type: FileWriter
    _storage = None  # type: BaseStorage

    def __init__(self, storage, path='data/backgrounds'):
        self._path = path
        self._storage = storage

    @property
    def writer(self) -> FileWriter:
        """
        Image writer.

        :return: BaseImageWriter object
        :rtype: BaseImageWriter

        """
        if not self._writer:
            self._writer = self.writer_class(storage=self._storage)
        return self._writer

    @property
    def reader(self) -> ImageReader:
        """
        Image reader.

        :return: BaseImageReader object
        :rtype: BaseImageReader

        """
        if not self._reader:
            self._reader = self.reader_class(path=self._path, storage=self._storage)
        return self._reader


class Backgrounds(AbstractBackgrounds):
    """
    Backgrounds class.

    """
    writer_class = FileWriter
    reader_class = ImageReader
