# Contributing

Thanks for contributing to E‑MediCenter!

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

cp .env.example .env
# edit .env and set DJANGO_SECRET_KEY

python3 manage.py migrate
python3 manage.py seed_demo --clear
python3 manage.py runserver
```

## Running tests

```bash
python3 manage.py test
```

## Pull requests

- Create a focused PR (one topic per PR).
- Include a clear description of the change and why it’s needed.
- For UI changes, include screenshots/GIFs when possible.
- Ensure `python3 manage.py test` passes.

## Secrets & data

- Never commit `.env`, API keys, or credentials.
- Never commit real personal/medical data.
- Before pushing, quickly scan for common secret patterns:

```bash
rg -n -e "A\\s*I\\s*z\\s*a" -e "django\\s*-\\s*insecure" -e "sk-[A-Za-z0-9]{10,}" -S .
```

## Reporting issues

- Use GitHub Issues for bugs and feature requests.
- Include steps to reproduce, expected/actual behavior, and relevant logs.
