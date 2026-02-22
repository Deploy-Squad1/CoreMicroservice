# CoreMicroservice

## How to set up pre-commit hooks

1. Install pre-commit from <https://pre-commit.com/#install>
2. Run `pre-commit install`
3. Auto-update the config to the latest version `pre-commit autoupdate`

## Setup project

### Create virtual environment and install dependencies

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

### Create .env file

Create .env file in the root directory with all the secrets:

```bash
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
DB_HOST=""
DB_PORT=""

DJANGO_SECRET_KEY=""
```

### Load environment variables from .env file

```bash
set -a
source .env
set +a
```

### Apply migrations

Run `flask db upgrade`

### Run application

Run `python manage.py runserver`
