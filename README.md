## Description

Lost & Found App built with FastAPI, designed to help users report, and recover lost or found items in public spaces. The app includes features for item reporting, smart matching, photo uploads, user comments, and audit logging.

## Features
📦 Report Lost or Found Items – Users can create posts with descriptions, images, locations, and timestamps.

🔍 Matching Engine – The backend supports logic to detect and suggest possible matches between lost and found reports.

🖼️ Photo Uploads – Users can attach photos to enhance identification.


## Tech Stack
Backend: FastAPI

ORM: SQLAlchemy

Validation: Pydantic

Database: PostgreSQL (or SQLite for development)

Containerization: Docker

File Storage: minIO

### Local Development

This project utilizes `Python` and is built on [FastAPI](https://fastapi.tiangolo.com/).
[Poetry](https://python-poetry.org/) is used for dependency management and development.

### Libraries which are needed but not included in the Python virtual env:

#### If using a Mac, please run

- `brew install libmagic`

#### If running an Ubuntu machine, please run

```sh
sudo apt-get install libmagic-dev
```

### Optional: Setup Pyenv

#### Install Pyenv

[Pyenv](https://github.com/pyenv/pyenv) is a useful Python version manager that allows you to easily switch between
multiple versions of python without having to mess with your system-wide installations.

To install `pyenv`, simply run the following:

```console
$ brew update
$ brew install pyenv
```

You may also need to set the following in your `.zshrc` if it is not already there (assuming you are using zshell):

```
eval "$(pyenv init -)"
```

Additionally, the following should be set in your `.zprofile`

```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
```

> Note: These files should exist in your home directory

Alternatively, you may install Python directly or via other means. Pyenv is simply a suggestion.

#### Install Python

The python version should automatically be picked up by the `.python-version` file. If you haven't already, you can
install the specified version of python via the following command:

```console
$ pyenv install
```

> If this happens, try running the following patch (replace <python_version> with the project's version of Python):

```console
$ CFLAGS="-I$(brew --prefix openssl)/include -I$(brew --prefix bzip2)/include -I$(brew --prefix readline)/include -I$(xcrun --show-sdk-path)/usr/include" LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix readline)/lib -L$(brew --prefix zlib)/lib -L$(brew --prefix bzip2)/lib" pyenv install --patch <python_version>
 < <(curl -sSL https://github.com/python/cpython/commit/8ea6353.patch\?full_index\=1)
```

> Note: If you cannot get pyenv to pickup the `.python-version` file, try installing manually (replace <python_version> with the project's version of Python):

```console
$ pyenv install <python_version>
```

### Set Up Python Virtual Environment

This project utilizes [Poetry](https://python-poetry.org/) for dependency management. The latest supported version is 1.5.1.

#### Install Poetry

1. [Install Poetry](https://python-poetry.org/docs/master/#installation) with the following command:

   ```console
   $ curl -sSL https://install.python-poetry.org | python3 - --version 1.5.1
   ```

1. After the poetry install, follow the output to update your `$PATH` environment variable.

1. By default, Poetry will create virtualenvs under `~/Library/Caches/pypoetry/virtualenvs/`. If you wish to install
   them in the project directory, add the following config:

   ```console
   $ poetry config virtualenvs.in-project true
   ```

1. You can verify the setting was changed with the following command:

   ```console
   $ poetry config virtualenvs.in-project
   ```

### Install Development Dependencies

1. Install [Docker](https://docs.docker.com/get-docker/)
1. Under Docker --> Preferences --> Resources --> Advanced, increase memory to ~8GB and ~4 CPUs
1. Apple Silicon Macs:  Docker --> Settings --> General --> Use Rosetta for x86/amd64 emulation on Apple Silicon.  Make sure the checkbox is checked. See [Docker 4.25](https://www.docker.com/blog/docker-desktop-4-25/) for more info.
1. Apple Silicon Macs: If the checkbox for Rosetta does not appear in Docker settings, check the MACOS version.  If macOS version is < 14.1, upgrade and try again.


### Configure Private Repositories & Docker Login

#### Configure Private Repositories

1. Follow the [Gitlab instructions](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) to setup a
   personal access token (only `read_api` access).

1. Run the following make command to setup the shared repository and provide your `read_api` access token when prompted:

   ```console
   $ make poetry-config
   ```

1. This will generate a `.env` file in the root project directory. Follow the prompt instructions and paste your token
   in the file.

> Note: This configures the Shared group and pihealth-api (fics-api) repositories.

#### Create Virtual Environment

1. If you do not have the python version specified in `.python-version` installed, make sure to do so before continuing. If using
   [pyenv](https://github.com/pyenv/pyenv), follow the steps in the previous section.

1. Run the following command to have Poetry create a virtualenv and install the necessary dependencies:

   ```console
   $ poetry install
   ```

   > Note: If this errors out due to missing psycopg[binaries], run `brew install postgresql` and retry

1. Activate the virtual environment:

   ```console
   $ poetry shell
   ```

   > Note: The default version of pip may be insufficient. If the install above fails, run the following to update pip and retry the install.

   ```console
   $ poetry run pip install --upgrade pip
   $ poetry install
   ```

### Start App in Docker

1. Run the following command to build and start the containers:

   ```console
   $ docker compose up -d
   ```

1. Access the API at http://localhost:8000/docs#/

> Note: Since the `app` codebase is mounted in the container, the app will automatically reload when changes to the
> code are detected.

### Setting up in VS Code

If you would like to use VS Code instead of PyCharm, here are some recommended steps

1. Install the recommended extensions (should be automatic)
1. Consider setting the following settings in your workspace `settings.json` (CMD + ,)

```json
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnType": true,
  },
  "python.analysis.autoFormatStrings": true,
  "python.analysis.autoImportCompletions": true,
  "python.analysis.typeCheckingMode": "basic",
  "python.formatting.provider": "yapf",
  "python.linting.mypyEnabled": true,
  "python.linting.pylintEnabled": true,
  "pylint.importStrategy": "fromEnvironment",
  "python.linting.ignorePatterns": [
    ".vscode/*.py",
    "**/site-packages/**/*.py",
    "alembic/**/*.py"
  ],
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests"
  ],
  "search.exclude": {
    "**/__pycache__": true,
    "**/.venv": true,
    "**/htmlcov": true
  }
```


## Spinning Up Local Backend Environment

Recommended way to spin up fresh, new local astro api backend environment:

```console
docker compose up
```

### Common Commands

The application can always be rebuilt at any time independently using the following command,
this is typically run in the following scenarios:

- when there are changes to the python dependencies (such as in poetry)
- when there is a change to the sample data

```console
docker compose up --build
```

### Log viewing

At any time, to view the back-end logs, run the following command:

```console
docker compose logs -ft
```

---

### ENV file setup

Create .env file in the root folder and 

```
DATABASE_URL=postgresql+psycopg://postgres:password@db:5432/lost_found_db
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=lost_found_db 
PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin
MINIO_ENDPOINT = localhost:9000
MINIO_ACCESS_KEY = minioadmin
MINIO_SECRET_KEY = minioadmin
MINIO_BUCKET_NAME = lostfound-images
MINIO_SECURE = False  # local, no HTTPS
API_KEY<YOUR_API_KEY>
```
