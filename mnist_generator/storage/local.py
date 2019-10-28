"""
Local storage class.

"""
import os
from typing import Union, List

from .base import BaseStorage


class LocalStorage(BaseStorage):
    """
    Local storage class.

    """
    def count(self, path: str) -> int:
        """
        Get count files in path.

        :param str path: Path for calculate count objects.

        :return: Count objects
        :rtype: int

        """
        if os.path.isfile(path):
            return 1
        path, dirs, files = next(os.walk(path))
        return len(files)

    def read(self, path: str, mode: str = 'rb') -> Union[bytes, str]:
        """
        Read file from storage

        :param str path: Path to file in storage.
        :param str mode: Mode open file

        :return: File Bytes.
        :rtype: Union[bytes, str]

        """
        with open(path, mode=mode) as f:
            return f.read()

    def write(self, path: str, file_bytes: bytes):
        """
        Write file to storage.

        :param str path: Path to file.
        :param bytes file_bytes: Bytes for file.

        """
        with open(path, 'wb') as f:
            f.write(file_bytes)

    def list(self, path: str) -> List[str]:
        """
        Get list files from path.

        :param str path: Path for search.

        :return: List filenames
        :rtype: List[str]

        """
        return [os.path.join(path, file_name) for file_name in os.listdir(path)]
