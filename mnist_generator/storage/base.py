"""
Storage vase classes.

"""
import abc
import os
from typing import List, Union, Generator


class BaseStorage(abc.ABC):
    """
    Base Storage reader.

    """
    @abc.abstractmethod
    def count(self, path: str) -> int:
        """
        Get count files in path.

        :param str path: Path for calculate count objects.

        :return: Count objects
        :rtype: int

        """
        pass

    @abc.abstractmethod
    def list(self, path: str) -> List[str]:
        """
        Get list files from path.

        :param str path: Path for search.

        :return: List filenames
        :rtype: List[str]

        """
        pass

    @abc.abstractmethod
    def read(self, path: str, mode: str = 'rb') -> Union[bytes, str]:
        """
        Read file from storage

        :param str path: Path to file in storage.
        :param str mode: Mode open file

        :return: File Bytes.
        :rtype: Union[bytes, str]

        """
        pass

    @abc.abstractmethod
    def write(self, path: str, file_bytes: bytes):
        """
        Write file to storage.

        :param str path: Path to file.
        :param bytes file_bytes: Bytes for file.

        """
        pass


class BaseFileChecker(object):
    """
    Base file checker.

    """
    def ignore(self, file_path: str) -> bool:
        """
        Ignore file?

        :param str file_path: Path to file.

        :return: Result check
        :rtype: bool

        """
        return False


class FileReader(object):
    """
    Base file reader.

    """
    storage = None  # type: BaseStorage
    file_checker = BaseFileChecker()  # type: BaseFileChecker
    file_mode = 'rb'

    def __init__(self, path: str, storage: BaseStorage = None,
                 file_checker: BaseFileChecker = None, file_mode: str = 'rb'):
        """
        File reader.

        :param str path: Path to folder for files.
        :param storage.base.BaseStorage storage: Storage class.
        :param storage.base.BaseFileChecker file_checker: File checker.
        :param str file_mode: Mode open file. Default rb

        """
        self._path = path
        self.storage = storage or self.storage
        self.file_checker = file_checker or self.file_checker
        self.file_mode = file_mode

    def __len__(self) -> int:
        return self.storage.count(self._path)

    def get_files_patches_from_storage(self) -> Generator[str, None, None]:
        """
        Get files patches from storage.

        :return: File patches generator
        :rtype: Generator[str, None, None]

        """
        for file_path in self.storage.list(self._path):
            if not self.file_checker.ignore(file_path):
                yield file_path

    def get_files_from_storage(self) -> Generator[Union[str, bytes], None, None]:
        """
        Get files from storage.

        :return: File bytes generator
        :rtype: Generator[Union[str, bytes], None, None]

        """
        for file_path in self.get_files_patches_from_storage():
            yield self.storage.read(file_path, mode=self.file_mode)


class FileWriter(object):
    """
    Base writer for files.

    """
    storage = None  # type: BaseStorage

    def __init__(self, path: str, storage: BaseStorage):
        """
        Base image writer.

        :param str path: Path to base folder.
        :param BaseStorage storage: Storage class for backgrounds.

        """
        self.path = path
        self.storage = storage or self.storage

    def write(self, path: str, file_bytes: bytes):
        """
        Write data to file.

        :param str path: Path to save file
        :param bytes file_bytes: File bytes for write.

        """
        self.storage.write(path=os.path.join(self.path, path), file_bytes=file_bytes)
