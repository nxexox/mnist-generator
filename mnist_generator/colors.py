"""
Colors reader

"""
from dataclasses import dataclass
from mnist_generator.storage import FileReader


@dataclass
class Color(object):
    """
    Color object.

    """
    red: int
    green: int
    blue: int

    def to_tuple(self):
        """
        Return tuple color in RGB format.

        :return: Tuple rgb color
        :rtype: tuple

        """
        return self.red, self.green, self.blue


class ColorsReader(FileReader):
    """
    Colors reader.

    """
    line_separator = '\n'
    color_separator = ','

    def row_to_color(self, row):
        """
        Row to color.

        :param str row: Source row from file.

        :return: Color object
        :rtype: Color

        """
        rgb = row.split(self.color_separator)
        return Color(red=int(rgb[0]), green=int(rgb[1]), blue=int(rgb[2]))

    def get_colors(self):
        """
        Get colors.

        :return: Iterable colors
        :rtype: Generator[Color, None, None]

        """
        text_file = self.storage.read(self._path, mode='r')

        for row in text_file.split(self.line_separator):
            yield self.row_to_color(row)
