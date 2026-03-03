# Константи
DOCKER_COMPOSE = docker compose
BACKEND_CONTAINER = backend
PYTHON = uv run python
MANAGE_PY = manage.py


.PHONY: up
up: ## Запустити всі контейнери
	$(DOCKER_COMPOSE) up -d

.PHONY: down
down: ## Зупинити всі контейнери
	$(DOCKER_COMPOSE) down

.PHONY: build
build: ## Зібрати Docker образи
	$(DOCKER_COMPOSE) build

.PHONY: rebuild
rebuild: ## Пересібрати образи та запустити
	$(DOCKER_COMPOSE) up -d --build

.PHONY: shell
shell: ## Відкрити командний рядок контейнера бекенду
	docker exec -it $(BACKEND_CONTAINER) sh

.PHONY: bash
bash: ## Відкрити bash в контейнері бекенду
	docker exec -it $(BACKEND_CONTAINER) bash

.PHONY: makemigrations
makemigrations: ## Створити міграції Django
	docker exec -it $(BACKEND_CONTAINER) $(PYTHON) $(MANAGE_PY) makemigrations

.PHONY: migrate
migrate: ## Застосувати міграції Django
	docker exec -it $(BACKEND_CONTAINER) $(PYTHON) $(MANAGE_PY) migrate

.PHONY: createsuperuser
createsuperuser: ## Створити суперкористувача Django
	docker exec -it $(BACKEND_CONTAINER) $(PYTHON) $(MANAGE_PY) createsuperuser

.PHONY: collectstatic
collectstatic: ## Зібрати статичні файли
	docker exec -it $(BACKEND_CONTAINER) $(PYTHON) $(MANAGE_PY) collectstatic --noinput

.PHONY: shell-django
shell-django: ## Відкрити Django shell
	docker exec -it $(BACKEND_CONTAINER) $(PYTHON) $(MANAGE_PY) shell

.PHONY: test
test: ## Запустити тести
	docker exec -it $(BACKEND_CONTAINER) $(PYTHON) $(MANAGE_PY) test