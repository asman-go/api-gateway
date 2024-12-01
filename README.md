# api-gateway
Asman Compute Engine API Gateway

# Build docker image

```
$ make build
$ make push
```

# Develope

## Prepare python venv

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

## Deploy local: build & run

```
~ docker compose -f deploy/docker-compose.yml build
~ docker compose -f deploy/docker-compose.yml up
```

Go to:

- http://localhost:7860/healthcheck
- http://localhost:7860/example

## Run tests

Поднимаем тестовую базу (для use-case'ов нужна)

```
~ docker compose -f deploy/testing.docker-compose.yml up
```

Запускаем сами тесты:

```
~ python -m pytest .
```

### Errors

```
ERROR src/gateway/tests - ImportError: cannot import name 'runtime_version' from 'google.protobuf'
```

Гипотеза: версия protoc/protobuf в OS и в зависимостях различаются. Решать пока это не хочу

Частное решение: идем в `.venv/lib/.../asman/domains/example/api/schema_pb2.py` и убираем вручную все, что упоминает `_runtime_version`. Перезапускаем тесты.


# TODO

[hatch-requirements-txt](https://github.com/repo-helper/hatch-requirements-txt) не поддерживает зависимости на git репозитории. Поэтому пока устанавливаю зависимости на свои репозитории из `Docker`-файла, сами зависимости прописал в `requirements.git.txt`.
