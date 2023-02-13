IMAGE:=aaa-frontend

help:
	@echo "help - show this help"
	@echo "run - start application"
	@echo "dev - start application in dev mode with live reload"
	@echo "build - build docker image"


build:
	@docker build -t ${IMAGE} .

dev:
	@docker run -v $(PWD):/app \
		-p 127.0.0.1:8080:8080 \
		-p 127.0.0.1:8081:8081 \
		-it ${IMAGE} \
		adev runserver --livereload --host 0.0.0.0 --port 8080 run.py

run:
	@docker run -it -p 127.0.0.1:8080:8080 ${IMAGE}
	

test:
	@docker run --net=host -v $(PWD):/app -ti ${IMAGE} \
		python -m pytest --disable-warnings -v
