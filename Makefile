# Constants
DOCKER_COMPOSE = docker compose
BACKEND_CONTAINER = backend
PYTHON = uv run python
MANAGE_PY = manage.py


.PHONY: up
up: # Starts all containers
	$(DOCKER_COMPOSE) up -d

.PHONY: down
down: # Stop all containers
	$(DOCKER_COMPOSE) down

.PHONY: build
build: # Collect docker images
	$(DOCKER_COMPOSE) build

.PHONY: rebuild
rebuild: ## Rebuild the images and run
	$(DOCKER_COMPOSE) up -d --build

.PHONY: shell
shell: ## Open the backend container command line
	docker exec -it $(BACKEND_CONTAINER) sh

.PHONY: bash
bash: ## Open bash in the backend container
	docker exec -it $(BACKEND_CONTAINER) bash

.PHONY: makemigrations
makemigrations: ## Create Django migrations
	docker exec -it $(BACKEND_CONTAINER) $(PYTHON) $(MANAGE_PY) makemigrations

.PHONY: migrate
migrate: ## Apply Django migrations
	docker exec -it $(BACKEND_CONTAINER) $(PYTHON) $(MANAGE_PY) migrate

.PHONY: createsuperuser
createsuperuser: ## Create a Django superuser
	docker exec -it $(BACKEND_CONTAINER) $(PYTHON) $(MANAGE_PY) createsuperuser

.PHONY: collectstatic
collectstatic: ## Compile static files
	docker exec -it $(BACKEND_CONTAINER) $(PYTHON) $(MANAGE_PY) collectstatic --noinput

.PHONY: shell-django
shell-django: ## Open the Django shell
	docker exec -it $(BACKEND_CONTAINER) $(PYTHON) $(MANAGE_PY) shell

.PHONY: test
test: ## Run the tests
	docker exec -it $(BACKEND_CONTAINER) $(PYTHON) $(MANAGE_PY) test
