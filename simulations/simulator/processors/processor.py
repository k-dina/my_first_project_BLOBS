from abc import ABC, abstractmethod


class Processor(ABC):
    @abstractmethod
    def __init__(self, configuration):
        ...
