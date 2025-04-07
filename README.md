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

3. Activate the environment:

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
$pip install -e .
```

### Setup the environment variables

```bash
$cp .env.example .env
```

Then, set your environment variables in the `.env` file, and update values with your credentials.

## Setup MongoDB Database

### Pulling a MongoDB image

```bash
$docker pull mongodb/mongodb-community-server:latest
```

### Running a MongoDB container

```bash
$docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest
```

## Run the FastAPI Server

```bash
$uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## API Interaction Diagram

[![Initial API Interaction Diagram](https://mermaid.ink/img/pako:eNqtlUtrGzEQx7_KIMjNxvc9BPpKySHEjZseykJRpVmv2l1pqwdOMP7ulax9P-Ia6oNhpflrfvPXSDoSpjiShBj841Ay_CjoXtMyleB_FdVWMFFRaeHZoJ6O3okCDbzb3k-nPqiiQGaFkgsB95Lji5D7-dkdUs3ybi7-39zAc1UoyoFKDlutGBoDd4U6xPlAub69bbES2D7uvsImCwMbd5bGyDZk7eODLIEntE5LCLE_BF-BsdQ6k0BKohB5SsbiQa73uBcSqLOqpL4QqCKfr3GJ7vOnFu5Y5z1thMzUJchu6Rpz5NJjFZynRQIPVDpaNF69wdJ3qoOpE13B80v9nGf6JvDg20JalPYqQ1hfc5EBOVh8sTBQtRD9tpz0zahnG09YNxzDR3ETkk7g-a_MsDkO1KfoxoW83tVM6PLcuwYo58EE1eMYudCevYkF_VPZ0AnJBWsY-gGTwkWY7B2eGclwu9GemWF5i4dAvTO6sMFPuBZXVTfuNo1n_b-gu4pT663-PyXMO9tsbY21eOLrC3NScneRNgWb80gM6mYnnF8c6te4o77EN0n7Oery_A3I8hDCFXOlV5qZhCM7jRRVhdZAprSv17jCzl08M9lqunaFSa5xo0YPmiRwEDZvxWRFStQlFdw_jMewVEpsjiWmJDwGnOrf4SE4-bhw1-9eJSOJ1Q5XRCu3z0mS0cL4r9ge9ZPajvrn7btSzffpL1qxeoE?type=png)](https://mermaid.live/edit#pako:eNqtlUtrGzEQx7_KIMjNxvc9BPpKySHEjZseykJRpVmv2l1pqwdOMP7ulax9P-Ia6oNhpflrfvPXSDoSpjiShBj841Ay_CjoXtMyleB_FdVWMFFRaeHZoJ6O3okCDbzb3k-nPqiiQGaFkgsB95Lji5D7-dkdUs3ybi7-39zAc1UoyoFKDlutGBoDd4U6xPlAub69bbES2D7uvsImCwMbd5bGyDZk7eODLIEntE5LCLE_BF-BsdQ6k0BKohB5SsbiQa73uBcSqLOqpL4QqCKfr3GJ7vOnFu5Y5z1thMzUJchu6Rpz5NJjFZynRQIPVDpaNF69wdJ3qoOpE13B80v9nGf6JvDg20JalPYqQ1hfc5EBOVh8sTBQtRD9tpz0zahnG09YNxzDR3ETkk7g-a_MsDkO1KfoxoW83tVM6PLcuwYo58EE1eMYudCevYkF_VPZ0AnJBWsY-gGTwkWY7B2eGclwu9GemWF5i4dAvTO6sMFPuBZXVTfuNo1n_b-gu4pT663-PyXMO9tsbY21eOLrC3NScneRNgWb80gM6mYnnF8c6te4o77EN0n7Oery_A3I8hDCFXOlV5qZhCM7jRRVhdZAprSv17jCzl08M9lqunaFSa5xo0YPmiRwEDZvxWRFStQlFdw_jMewVEpsjiWmJDwGnOrf4SE4-bhw1-9eJSOJ1Q5XRCu3z0mS0cL4r9ge9ZPajvrn7btSzffpL1qxeoE)
