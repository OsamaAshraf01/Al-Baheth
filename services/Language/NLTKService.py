from .LanguageSevice import LanguageService
from fastapi import Depends
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
from typing import Literal

class NLTKService(LanguageService):
    
    # Static Attributes
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    
    def __init__(self):
        super().__init__()
    
    def tokenize(self, text: str) -> list[str]:
        """
        Tokenizes the input text into individual words.

        Args:
            text (str): The input string to be tokenized.

        Returns:
            list[str]: A list of words extracted from the input text.
        """
        return word_tokenize(self, text)
    
    def remove_stopwords(self, tokens: list[str]) -> list[str]:
        """
        Remove stopwords from a list of tokens.

        Args:
            tokens (list[str]): A list of tokens (words) from which stopwords need to be removed.

        Returns:
            list[str]: A new list containing only the tokens that are not stopwords.
        """
        return [token for token in tokens if token not in self.stop_words]
    
    def get_wordnet_pos(self, treebank_tag: str) -> Literal['a', 'v', 'n', 'r']:
        """
        Convert a Treebank part-of-speech tag to a WordNet part-of-speech tag.

        Args:
            treebank_tag (str): A part-of-speech tag in Treebank format.

        Returns:
            Literal['a', 'v', 'n', 'r']: The corresponding WordNet part-of-speech tag,
            which can be one of the following:
                - 'a' for adjectives
                - 'v' for verbs
                - 'n' for nouns
                - 'r' for adverbs

        If the input tag does not match any known categories, it defaults to returning
        the noun tag.
        """
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN
        
    def lemmatize(self, tokens) -> list[str]:
        """
        Lemmatizes a list of tokens using their part-of-speech tags.

        This method first tags each token with its corresponding part-of-speech (POS) 
        using the NLTK library. It then applies lemmatization to each token based on 
        its POS tag, which helps in reducing words to their base or dictionary form.

        Args:
            tokens (list[str]): A list of tokens (words) to be lemmatized.

        Returns:
            list[str]: A list of lemmatized tokens.
        """
        pos_tags = nltk.pos_tag(tokens)
        processed_tokens = [self.lemmatizer.lemmatize(token, self.get_wordnet_pos(pos)) for token, pos in pos_tags]  
        return processed_tokens
    
    def stem(self, tokens) -> list[str]:
        """
        Stems a list of tokens using the configured stemmer.

        Args:
            tokens (list[str]): A list of words (tokens) to be stemmed.

        Returns:
            list[str]: A list of stemmed words.
        """
        return [self.stemmer.stem(word) for word in tokens]
    
    