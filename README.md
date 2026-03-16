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

DEBUG=""            # False by default
ALLOWED_HOSTS=""    # Only serving on 127.0.0.1 by default

FRONTEND_SERVICE_URL=""
EMAIL_SERVICE_URL=""
MAP_SERVICE_BASE_URL=""
VOTING_SERVICE_URL=""
```

### Load environment variables from .env file

```bash
set -a
source .env
set +a
```

### Apply migrations

Run `python manage.py migrate`

### Create an initial passcode

Run `python manage.py rotate_passcode <initial_passcode>`

### Run application (development server)

Run `python manage.py runserver`
