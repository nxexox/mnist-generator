"""
Text parses.

"""
import abc
import re
from typing import Generator, Iterable


TEXT_PARSER_CHAR_MODE = 'chars'
TEXT_PARSER_WORDS_MODE = 'words'
TEXT_PARSER_SENTENCES_MODE = 'sentences'
TEXT_PARSER_PARAGRAPHS_MODE = 'paragraphs'
ALLOWED_TEXT_PARSE_MODES = (
    TEXT_PARSER_CHAR_MODE, TEXT_PARSER_WORDS_MODE,
    TEXT_PARSER_SENTENCES_MODE, TEXT_PARSER_PARAGRAPHS_MODE
)


class AbstractTextParser(abc.ABC):
    """
    Abstract text parser.

    """
    paragraph_separator = re.compile(r'\n')
    sentences_separator = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z][а-з][А-З]\.)(?<=\.|\?)\s')
    words_separator = re.compile(r' ')
    paragraph_separator_with_delimiter = re.compile(r'.*?{}'.format(paragraph_separator.pattern))
    sentences_separator_with_delimiter = re.compile(r'.*?{}'.format(sentences_separator.pattern))
    words_separator_with_delimiter = re.compile(r'.*?{}'.format(words_separator.pattern))

    _text_reader_modes = {
        'chars': 'get_chars',
        'words': 'get_words',
        'sentences': 'get_sentences',
        'paragraphs': 'get_paragraphs'
    }

    @classmethod
    def get_text_lines(cls, text: str) -> Generator[str, None, None]:
        """
        Get text lines for write to background.

        :param str text: Text for split by lines.

        :return: Generator text lines
        :rtype: Generator[str, None, None]

        """
        for row in text.split('\n'):
            yield row

    @classmethod
    def count_blocks(cls, text: str, mode: str, added_separator: bool = False) -> int:
        """
        Get count blocks.

        :param str text: Source text
        :param str mode: Parser mode
        :param bool added_separator: Added separator

        :return: Count texts blocks.
        :rtype: int

        """
        return len(list(cls.get_text_blocks(text=text, mode=mode, added_separator=added_separator)))

    @classmethod
    def get_text_blocks(cls, text: str, mode: str, added_separator: bool = False) -> Iterable[str]:
        """
        Get text blocks.

        :param str text: Source text
        :param str mode: Parser mode
        :param bool added_separator: Added separator

        :return: Text blocks.
        :rtype: Iterable[str]

        """
        try:
            parser_func_name = cls._text_reader_modes[mode]
        except KeyError:
            raise ValueError('mode={} not valid value. Valid values: {}'.format(
                mode, list(cls._text_reader_modes.keys())
            ))

        func = getattr(cls, parser_func_name)
        return func(text, added_separator)

    @classmethod
    @abc.abstractmethod
    def get_paragraphs(cls, text: str, added_separator: bool = False) -> Iterable[str]:
        """
        Get paragraphs from source text.

        :param str text: Source text
        :param bool added_separator: Added separator

        :return: Paragraphs text
        :rtype: Iterable[str]

        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_sentences(cls, text: str, added_separator: bool = False) -> Iterable[str]:
        """
        Get sentences from source text.

        :param str text: Source text
        :param bool added_separator: Added separator

        :return: Sentences text
        :rtype: Iterable[str]

        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_words(cls, text: str, added_separator: bool = False) -> Iterable[str]:
        """
        Get words from source text.

        :param str text: Source text
        :param bool added_separator: Added separator

        :return: Words text
        :rtype: Iterable[str]

        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_chars(cls, text: str, added_separator: bool = False) -> Iterable[str]:
        """
        Get chars from source text.

        :param str text: Source text
        :param bool added_separator: Added separator

        :return: Chars text
        :rtype: Iterable[str]

        """
        pass


class TextGeneratorParser(AbstractTextParser):
    """
    Text generator parser. Parsing source text and return generators.

    """

    @classmethod
    def get_paragraphs(cls, text: str, added_separator: bool = False) -> Generator[str, None, None]:
        """
        Get paragraphs from source text.

        :param str text: Source text
        :param bool added_separator: Added separator

        :return: Paragraphs text
        :rtype: Generator[str, None, None]

        """
        split_func = re.findall if added_separator else re.split
        split_reg = cls.paragraph_separator_with_delimiter if added_separator else cls.paragraph_separator
        for paragraph in split_func(split_reg, text):
            yield paragraph

    @classmethod
    def get_sentences(cls, text: str, added_separator: bool = False) -> Generator[str, None, None]:
        """
        Get sentences from source text.

        :param str text: Source text
        :param bool added_separator: Added separator

        :return: Sentences text
        :rtype: Generator[str, None, None]

        """
        split_func = re.findall if added_separator else re.split
        split_reg = cls.sentences_separator_with_delimiter if added_separator else cls.sentences_separator
        for sentence in split_func(split_reg, text):
            yield sentence

    @classmethod
    def get_words(cls, text: str, added_separator: bool = False) -> Generator[str, None, None]:
        """
        Get words from source text.

        :param str text: Source text
        :param bool added_separator: Added separator

        :return: Words text
        :rtype: Generator[str, None, None]

        """
        split_func = re.findall if added_separator else re.split
        split_reg = cls.words_separator_with_delimiter if added_separator else cls.words_separator
        for word in split_func(split_reg, text):
            yield word

    @classmethod
    def get_chars(cls, text: str, added_separator: bool = False) -> Generator[str, None, None]:
        """
        Get chars from source text.

        :param str text: Source text
        :param bool added_separator: Added separator

        :return: Chars text
        :rtype: Generator[str, None, None]

        """
        for char in text:
            yield char
