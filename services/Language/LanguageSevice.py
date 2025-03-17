from abc import ABC, abstractmethod
import re
from typing import Literal

class LanguageService(ABC):
    
    def normalize(text: str) -> str:
        """
        Normalize the input text by converting it to lowercase, 
        removing non-alphabetic characters, and reducing 
        multiple spaces to a single space.

        Args:
            text (str): The input string to be normalized.

        Returns:
            normalized_text (str): The normalized string with lowercase letters, 
            no non-alphabetic characters, and single spaces.
        """
        text = text.lower()
        text = re.sub("[^a-z ]+", " ", text).strip()
        text = re.sub("\s+", " ", text).strip()
        return text

    @abstractmethod
    def tokenize(self, text: str) -> list[str]:
        """
        Tokenizes the input text into individual words.

        Args:
            text (str): The input string to be tokenized.

        Returns:
            list[str]: A list of words extracted from the input text.
        """
        pass

    @abstractmethod    
    def remove_stopwords(self, tokens: list[str]) -> list[str]:
        """
        Remove stopwords from a list of tokens.

        Args:
            tokens (list[str]): A list of tokens (words) from which stopwords need to be removed.

        Returns:
            list[str]: A new list containing only the tokens that are not stopwords.
        """
        pass
    
    @abstractmethod
    def lemmatize(self, tokens : list[str]) -> list[str]:
        """
        Lemmatizes a list of tokens using their part-of-speech tags.

        This method first tags each token with its corresponding part-of-speech (POS). 
        It then applies lemmatization to each token based on its POS tag,
        which helps in reducing words to their base or dictionary form.

        Args:
            tokens (list[str]): A list of tokens (words) to be lemmatized.

        Returns:
            list[str]: A list of lemmatized tokens.
        """
        pass
    
    @abstractmethod
    def stem(self, tokens) -> list[str]:
        """
        Stems a list of tokens using the configured stemmer.

        Args:
            tokens (list[str]): A list of words (tokens) to be stemmed.

        Returns:
            list[str]: A list of stemmed words.
        """
        pass
    
    