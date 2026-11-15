# lovelace-chat

Chat backend for the Lovelace chat integration project.

## How to run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8001
```

The server runs at http://localhost:8001

## Redis

By default the chat uses an in-memory channel layer. It only works with one server process which is enough for development.
For deployment, set `REDIS_URL` so that all server processes share messages through Redis ->

```bash
REDIS_URL=redis://localhost:6379/3 python manage.py runserver 0.0.0.0:8001
```