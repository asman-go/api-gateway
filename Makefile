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
	@docker compose -f deploy/tests/docker-compose.yml build
	@docker compose -f deploy/tests/docker-compose.yml up

test:
	@python -m pip install -r requirements.test.txt
	@python -m pytest .
