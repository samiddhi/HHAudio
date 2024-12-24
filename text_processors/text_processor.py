from abc import ABC, abstractmethod
from aksharamukha import transliterate

class ITextProcessor(ABC):
    @abstractmethod
    def process_text(self, text: str) -> str:
        """
        Process text and apply necessary transformations for the specific language.
        """
        pass
