# lovelace-chat

Chat backend for the Lovelace chat integration project.

## How to run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The server runs at http://127.0.0.1:8000