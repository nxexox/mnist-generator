"""
Base classes for generations algorithms.

"""
import abc


class BaseAlgorithm(abc.ABC):
    """
    Base class for Algorithm.

    """
    @abc.abstractmethod
    def run(self):
        pass
