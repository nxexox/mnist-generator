"""
Image to storage saver.

"""
import io
import os

from PIL import Image

from mnist_generator.storage import FileWriter


class ImageToIoBytesWriter(FileWriter):
    """
    Image writer uses io.BytesIo for write for buffer storage, next send to write method in storage.

    """
    def write(self, path: str, file_bytes: Image.Image):
        """
        Save image to storage.

        :param str path: Image name for save.
        :param PIL.Image.Image file_bytes: Image object for save

        """
        img = file_bytes
        bytes_stream = io.BytesIO()
        img.save(bytes_stream, format=img.format)
        bytes_stream.seek(0)
        self.storage.write(os.path.join(self.path, path), bytes_stream.getvalue())
