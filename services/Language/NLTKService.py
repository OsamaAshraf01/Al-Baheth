from .LanguageProcessingService import LanguageProcessingService
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
from typing import Literal, List

class NLTKService(LanguageProcessingService):
    
    # Static Attributes
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    
    def __init__(self):
        super().__init__()
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenizes the input text into individual words.

        Args:
            text (str): The input string to be tokenized.

        Returns:
            List[str]: A List of words extracted from the input text.
        """
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords from a List of tokens.

        Args:
            tokens (List[str]): A List of tokens (words) from which stopwords need to be removed.

        Returns:
            List[str]: A new List containing only the tokens that are not stopwords.
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
        
    def lemmatize(self, tokens) -> List[str]:
        """
        Lemmatizes a List of tokens using their part-of-speech tags.

        This method first tags each token with its corresponding part-of-speech (POS) 
        using the NLTK library. It then applies lemmatization to each token based on 
        its POS tag, which helps in reducing words to their base or dictionary form.

        Args:
            tokens (List[str]): A List of tokens (words) to be lemmatized.

        Returns:
            List[str]: A List of lemmatized tokens.
        """
        pos_tags = nltk.pos_tag(tokens)
        processed_tokens = [self.lemmatizer.lemmatize(token, self.get_wordnet_pos(pos)) for token, pos in pos_tags]  
        return processed_tokens
    
    def stem(self, tokens) -> List[str]:
        """
        Stems a List of tokens using the configured stemmer.

        Args:
            tokens (List[str]): A List of words (tokens) to be stemmed.

        Returns:
            List[str]: A List of stemmed words.
        """
        return [self.stemmer.stem(word) for word in tokens]
    
    