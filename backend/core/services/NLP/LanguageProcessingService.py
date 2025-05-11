import re
import unicodedata
from abc import ABC, abstractmethod
from typing import List


class LanguageProcessingService(ABC):

    def normalize(self, text: str) -> str:
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
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def semantic_processing(self, text: str) -> str:
        """
        Processes the input text by performing semantic normalization. This includes
        removing HTML tags, converting text to lowercase, normalizing Unicode
        characters, and stripping extra whitespace.
        Semantic Processing does not include tokenization, stopword removal, lemmatization, or stemming.

        :param text: The input text to be processed.
        :return: A semantically normalized string processed as per the specified operations.
        """
        text = unicodedata.normalize('NFKC', text)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @abstractmethod
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenizes the input text into individual words.

        Args:
            text (str): The input string to be tokenized.

        Returns:
            List[str]: A List of words extracted from the input text.
        """
        pass

    @abstractmethod
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords from a List of tokens.

        Args:
            tokens (List[str]): A List of tokens (words) from which stopwords need to be removed.

        Returns:
            List[str]: A new List containing only the tokens that are not stopwords.
        """
        pass

    @abstractmethod
    def lemmatize(self, tokens: List[str]) -> List[str]:
        """
        Lemmatizes a List of tokens using their part-of-speech tags.

        This method first tags each token with its corresponding part-of-speech (POS). 
        It then applies lemmatization to each token based on its POS tag,
        which helps in reducing words to their base or dictionary form.

        Args:
            tokens (List[str]): A List of tokens (words) to be lemmatized.

        Returns:
            List[str]: A List of lemmatized tokens.
        """
        pass

    @abstractmethod
    def stem(self, tokens) -> List[str]:
        """
        Stems a List of tokens using the configured stemmer.

        Args:
            tokens (List[str]): A List of words (tokens) to be stemmed.

        Returns:
            List[str]: A List of stemmed words.
        """
        pass
