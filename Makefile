IMAGE:=aaa-frontend

help:
	@echo "help - show this help"
	@echo "run - start application"
	@echo "dev - start application in dev mode with live reload"
	@echo "build - build docker image"


build:
	@docker build -t ${IMAGE} .

dev:
	@docker run -v $(PWD):/app -p 127.0.0.1:8080:8080 -it ${IMAGE} \
		python -m gunicorn lib.app:async_create_app --bind 0.0.0.0:8080 \
		--reload --worker-class aiohttp.GunicornWebWorker

run:
	@docker run -it -p 127.0.0.1:8080:8080 ${IMAGE}
	

test:
	@docker run --net=host -v $(PWD):/app -ti ${IMAGE} \
		python -m pytest --disable-warnings -v
