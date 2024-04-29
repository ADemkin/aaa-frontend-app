IMAGE:=aaa-frontend

help:
	@echo "help - show this help"
	@echo "build - build docker image"
	@echo "test - run tests"
	@echo "lint - run lining"
	@echo "run - start applicaion"
	@echo "dev - start applicaion in dev mode with live reload"

clean:
	@docker rmi -f ${IMAGE}

build:
	@docker build -t ${IMAGE} . --network=host

dev: build
	@echo 'Run dev server with live reload- refer to dev server address.'
	@docker run --rm \
		-v $(PWD):/app \
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

flake8: build
	@echo 'Run flake8'
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		python -m flake8 lib

pycodestyle: build
	@echo 'Run pycodestyle'
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		python -m pycodestyle lib

pylint: build
	@echo 'Run pylint'
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		python -m pylint lib

black: build
	@echo 'Run black'
	@docker run --rm -v $(PWD):/app -i ${IMAGE} \
		python -m black lib

lint: black flake8 pycodestyle pylint
