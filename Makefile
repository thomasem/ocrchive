SHELL := /usr/bin/env bash

DEV_COMPOSE_FILE := "docker-compose.dev.yaml"

define dev_docker_compose
	@source .env && docker compose -f $(DEV_COMPOSE_FILE) $1
endef

define dev_docker_compose_run
	$(call dev_docker_compose, run --remove-orphans $1)
endef

.env: .env.sample
	cp $< $@
	@echo "Copied .env.sample to .env"

dev: .env
	$(call dev_docker_compose, up --build --remove-orphans)

dev-down: .env
	$(call dev_docker_compose, down)

dev-db-shell: .env
	$(call dev_docker_compose, exec -it db psql -U $$OCRCHIVE_PG_USER)

dev-reset: .env
	$(MAKE) dev-down
	@sudo rm -rf .dev/

migrate-status: .env
	$(call dev_docker_compose_run, migrate status)

migrate-verify: .env
	$(call dev_docker_compose_run, migrate verify)

migrate-deploy: .env
	$(call dev_docker_compose_run, migrate deploy --verify)

