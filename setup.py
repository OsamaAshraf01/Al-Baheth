from setuptools import setup, find_packages
from helpers.config import get_settings
import nltk

def download_nltk_data():
    nltk.download("stopwords")
    nltk.download("wordnet")
    nltk.download("punkt")
    nltk.download("punkt_tab")
    nltk.download("averaged_perceptron_tagger")
    nltk.download("averaged_perceptron_tagger_eng")

download_nltk_data()

with open("requirements.txt") as f:
    REQUIREMENTS_TXT = f.read().splitlines()

APP_VERSION = get_settings().APP_VERSION

setup(
    name= "Al-Baheth",
    packages= find_packages(),
    install_requires= REQUIREMENTS_TXT,
    version= APP_VERSION,
    include_package_data=True,
    url="https://github.com/OsamaAshraf01/Al-Baheth",
)