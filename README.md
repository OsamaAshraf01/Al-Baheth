# Al-baheth Search Engine

This is a search engine that searches in your own files.

## Requirements

- Python 3.8 or later

### Install Python using MiniConda

1. Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/index.html)
2. Create a new environment using the following command:

```bash
$conda create -n al-baheth python=3.8
```

1. Activate the environment:

```bash
$conda activate al-baheth
```

### (Optional) Setup your command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$pip install -r requirements.txt
```

### Setup the environment variables

```bash
$cp .env.example .env
```

Then, set your environment variables in the `.env` file, and update values with your credentials.

## Run the FastAPI Server

```bash
$uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
