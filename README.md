# api-gateway
Asman Compute Engine API Gateway

# Project: build

Python >= 3.10

```
~ python3 -m venv .venv
~ source .venv/bin/activate
~ python -m pip install -r requirements.git.txt
~ python -m pip install "."
```

Чтобы удалить зависимости из .venv окружения:

```
~ python -m pip uninstall asman-api-gateway
~ python -m pip uninstall asman
```

# Deploy: build & run

```
~ docker compose -f deploy/docker-compose.yml build
~ docker compose -f deploy/docker-compose.yml up
```

Go to:

- http://localhost:7860/healthcheck
- http://localhost:7860/example

# TODO

[hatch-requirements-txt](https://github.com/repo-helper/hatch-requirements-txt) не поддерживает зависимости на git репозитории. Поэтому пока устанавливаю зависимости на свои репозитории из `Docker`-файла, сами зависимости прописал в `requirements.git.txt`.
