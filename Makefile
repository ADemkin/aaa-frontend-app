IMAGE:=aaa-frontend
LIB_FOLDER:=lib

help:
	@echo "help - show this help"
	@echo "build - build docker image"
	@echo "test - run tests"
	@echo "lint - run linting and formatting"
	@echo "ruff - run linting"
	@echo "format - run formatting"
	@echo "run - start applicaion"
	@echo "dev - start applicaion in dev mode with live reload"
	@echo "clean - remove docker image"

clean:
	@docker rmi -f ${IMAGE}

build:
	@docker build -t ${IMAGE} . --network=host

dev: build
	@echo 'Run dev server with live reload- refer to dev server address.'
	@docker run --rm -v $(PWD):/app \
		-p 0.0.0.0:8000:8000 \
		-p 0.0.0.0:8001:8001 \
		-it ${IMAGE} \
		adev runserver --livereload --host 0.0.0.0 --port 8000 run.py

run: build
	@docker run --rm -it -p 0.0.0.0:8000:8000 ${IMAGE}

test: build
	@echo 'Run tests'
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		python -m pytest --disable-warnings -v

ruff: build
	@echo 'Run ruff lint'
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		ruff check ${LIB_FOLDER} $(if $(CI),,--fix)

format: build
	@echo 'Run ruff format'
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		ruff format ${LIB_FOLDER} $(if $(CI),--check,)

lint: ruff format

.PHONY: help clean build dev run test ruff format lint
