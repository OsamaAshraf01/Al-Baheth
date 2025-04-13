import sys
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

# --- NLTK Download Function ---
def download_nltk_data_internal():
    """Downloads required NLTK data corpora."""
    datasets = [
        "stopwords",
        "wordnet",
        "punkt",
        "punkt_tab",
        "averaged_perceptron_tagger",
        "averaged_perceptron_tagger_eng"
    ]
    print("--------------------------------------------------")
    print("Attempting to download required NLTK data...")
    print(f"Datasets to download: {', '.join(datasets)}")
    print("--------------------------------------------------")
    
    all_downloaded = True
    try:
        # Import nltk HERE, only when needed, after installation
        import nltk
        
        for dataset in datasets:
            try:
                print(f"\n>>> Checking/downloading NLTK dataset: {dataset}")
                nltk.download(dataset) # Let nltk handle checking if already downloaded
            except FileExistsError:
                 print(f"    Dataset '{dataset}' already exists.")
            except Exception as e:
                print(f"    ERROR downloading NLTK data '{dataset}': {e}", file=sys.stderr)
                print("    Please try manually: python -m nltk.downloader [dataset_name]")
                all_downloaded = False

    except ImportError:
        print("\nERROR: 'nltk' package not found. Cannot download NLTK data.", file=sys.stderr)
        print("       Please ensure 'nltk' is listed in requirements.txt or install_requires.", file=sys.stderr)
        all_downloaded = False
    except Exception as e:
        print(f"\nAn unexpected error occurred during NLTK download: {e}", file=sys.stderr)
        all_downloaded = False

    print("--------------------------------------------------")
    if all_downloaded:
        print("NLTK data download process completed.")
    else:
        print("NLTK data download process completed with errors (see above).")
    print("--------------------------------------------------")


# --- Custom Post-Installation Commands ---

class PostCommandMixin:
    """Mixin to run NLTK download after installation."""
    def run_nltk_download(self):
        # Run the download function in a separate process to ensure
        # it uses the final installed environment's NLTK, although
        # importing directly *should* work after super().run().
        # Using subprocess adds robustness but is slightly more complex.
        # For simplicity here, we'll try direct import first.
        download_nltk_data_internal()

    def run(self):
        # Run the standard command first
        super().run()
        # Then run our custom post-install step
        self.run_nltk_download()


class PostDevelopCommand(PostCommandMixin, develop):
    """Post-installation for development mode (`pip install -e .`)."""
    pass


class PostInstallCommand(PostCommandMixin, install):
    """Post-installation for standard mode (`pip install .`)."""
    pass



def get_app_verion(env_path="core/.env"):
    try:
        with open(env_path) as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("APP_VERSION="):
                app_verion = line.strip().split("=", 1)[1]
                app_verion = app_verion.replace('"', '').replace("'", "").strip()
                return app_verion
                
    except FileNotFoundError:
        raise RuntimeError("'.env' file not found or APP_VERSION not set")

APP_VERSION = get_app_verion()

# --- Read requirements.txt ---
try:
    with open("requirements.txt", encoding="utf-8") as f:
        REQUIREMENTS_TXT = f.read().splitlines()
    # Ensure nltk is in requirements if using this method!
    if not any(req.startswith('nltk') for req in REQUIREMENTS_TXT):
        print("Warning: 'nltk' dependency not found in requirements.txt.", file=sys.stderr)
        print("         NLTK data download during install might fail.", file=sys.stderr)
except FileNotFoundError:
    print("Warning: requirements.txt not found. Proceeding without install_requires.", file=sys.stderr)
    REQUIREMENTS_TXT = []


# --- Setup Configuration ---
setup(
    name="Al-Baheth",
    version=APP_VERSION, 
    packages=find_packages(),
    install_requires=REQUIREMENTS_TXT, 
    include_package_data=True,
    url="https://github.com/OsamaAshraf01/Al-Baheth",
    author="Your Name",
    author_email="your.email@example.com",
    description="This is a search engine that searches in your own files.",

    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)