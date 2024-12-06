IMAGE_NAME = "api-gateway"
IMAGE_VERSION = "1.5"

IMAGE_REGISTRY = "cr.yandex/crpnqn6joccbivjbkb27"

IMAGE_REPOSITORY = ${IMAGE_REGISTRY}/${IMAGE_NAME}
IMAGE_FULL_NAME = ${IMAGE_REPOSITORY}:${IMAGE_VERSION}


hello:
	@echo 'Build the Asman API Gateway docker image'
	@echo 'Push the image to a Docker registry'

deps:
	@echo 'Переустанавливаем зависимости'
	@python -m pip uninstall -y asman-api-gateway
	@python -m pip uninstall -y asman

	@python -m pip install -r requirements.git.txt
	@python -m pip install "."

l-deploy:
	@echo 'Поднимаем приложение локально'
	@docker compose -f deploy/docker-compose.yml build
	@docker compose -f deploy/docker-compose.yml up

t-deploy:
	@echo 'Поднимаем окружение для тестов'
	@docker compose -f deploy/testing.docker-compose.yml up

test:
	@python -m pytest .

build:
	@echo 'Собираем докер-образ с гейтвеем'
	@docker buildx build --no-cache -f deploy/Dockerfile -t ${IMAGE_FULL_NAME} .

push:
	@echo 'Загружаем образ в registry'
	@docker push ${IMAGE_FULL_NAME}
	@echo 'Загрузили образ: ${IMAGE_FULL_NAME}'
