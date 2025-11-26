PROJECT_NAME=mateup-league-app
DOCKER_COMPOSE=docker-compose
FRONTEND_BUILD_DIR=frontend-output
NGINX_HTML_DIR=/var/www/$(PROJECT_NAME)/html
BACKUP_DIR=./backups

# BASIC COMMANDS

test-make:
	echo "Project: $(PROJECT_NAME) - ✅ Deploy completed!"
up:
	$(DOCKER_COMPOSE) up -d --build

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f

back-logs:
	$(DOCKER_COMPOSE) logs -f backend

front-logs:
	$(DOCKER_COMPOSE) logs -f frontend

db-logs: 
	$(DOCKER_COMPOSE) logs -f db

restart:
	$(DOCKER_COMPOSE) down && $(DOCKER_COMPOSE) up -d --build

# INDIVIDUAL
frontend:
	$(DOCKER_COMPOSE) up -d --build frontend

backend:
	$(DOCKER_COMPOSE) up -d --build backend

# DATABASE
db:
	$(DOCKER_COMPOSE) up -d db

backup-db:
	$(DOCKER_COMPOSE) exec -T db sh -c 'PGPASSWORD=$$POSTGRES_PASSWORD pg_dump -U $$POSTGRES_USER $$POSTGRES_DB > $(BACKUP_DIR)/backup_$$(date +"%Y-%m-%d_%H-%M-%S").sql'

# make restore-db FILE=backup_2025-08-31_23-22-46.sql
restore-db:
	$(DOCKER_COMPOSE) exec -T db sh -c 'PGPASSWORD=$$POSTGRES_PASSWORD psql -U $$POSTGRES_USER $$POSTGRES_DB < $(BACKUP_DIR)/$(FILE)'

# DROP ALL TABLES OF DATABASE
drop-tables:
	$(DOCKER_COMPOSE) exec -T db sh -c 'PGPASSWORD=$$POSTGRES_PASSWORD psql -U $$POSTGRES_USER $$POSTGRES_DB -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO $$POSTGRES_USER; GRANT ALL ON SCHEMA public TO public;"'

list-tables:
	$(DOCKER_COMPOSE) exec -T db sh -c 'PGPASSWORD=$$POSTGRES_PASSWORD psql -U $$POSTGRES_USER $$POSTGRES_DB -c "\\dt"'

migrate:
	$(DOCKER_COMPOSE) run --rm backend poetry run alembic upgrade head

check-migrations:
	$(DOCKER_COMPOSE) run --rm backend poetry run alembic check

# RESET DATABASE (⚠️ WARNING: ALL DATA WILL BE LOST)
reset-db:
	$(DOCKER_COMPOSE) down -v
	$(DOCKER_COMPOSE) up -d --build

# JOBS
# Backup db - at 3am on Sunday
setup-cron:
	@echo "0 3 * * 0 cd $$(pwd) && make backup-db" | crontab -
	@echo "Cron job criado. Verifique com: crontab -l"

jobs:
	crontab -l

# EXECUTE IN CONTAINER
bash-frontend:
	$(DOCKER_COMPOSE) exec frontend sh

bash-backend:
	$(DOCKER_COMPOSE) exec backend bash

bash-db:
	$(DOCKER_COMPOSE) exec db bash

# INSTALL BACKEND DEPS (FastAPI w/ Poetry)
install-backend-deps:
	$(DOCKER_COMPOSE) run --rm backend poetry install

# INSTALL FRONTEND DEPS (Vite/Node)
install-frontend-deps:
	$(DOCKER_COMPOSE) run --rm frontend npm install

# 🔧 FRONTEND BUILD INSIDE CONTAINER AND MAKE A COPY TO ./frontend-output
build-frontend-copy:
	rm -rf $(FRONTEND_BUILD_DIR)
	mkdir -p $(FRONTEND_BUILD_DIR)
	$(DOCKER_COMPOSE) run --rm frontend sh -c "npm run build && cp -r dist/* /app/output"
	sleep 2

# 🔄 COPY TO NGINX FOLDER
deploy-frontend:
	sudo rm -rf $(NGINX_HTML_DIR)
	sudo mkdir -p $(NGINX_HTML_DIR)
	sudo cp -r $(FRONTEND_BUILD_DIR)/* $(NGINX_HTML_DIR)/

# 🚀 EXEC ALL: BUILD + COPY + RELOAD NGINX
deploy: migrate build-frontend-copy deploy-frontend
	sudo systemctl reload nginx
	
.PHONY: up down logs restart frontend backend db \
        bash-frontend bash-backend bash-db \
        reset-db install-backend-deps install-frontend-deps test-backend \
        migrate build-frontend-copy deploy-frontend deploy
