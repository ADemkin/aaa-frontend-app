@echo off

set IMAGE=aaa-frontend
set PWD=%cd%
IF /I "%1"=="IMAGE" GOTO IMAGE
IF /I "%1"=="help" GOTO help
IF /I "%1"=="build" GOTO build
IF /I "%1"=="dev" GOTO dev
IF /I "%1"=="run" GOTO run
IF /I "%1"=="test" GOTO test
IF /I "%1"=="flake8" GOTO flake8
IF /I "%1"=="pycodestyle" GOTO pycodestyle
IF /I "%1"=="pylint" GOTO pylint
IF /I "%1"=="lint" GOTO lint
GOTO error

@REM :IMAGE
@REM 	CALL make.bat =aaa-frontend
@REM 	GOTO :EOF

:help
	@echo "help - show this help"
	@echo "run - start application"
	@echo "dev - start application in dev mode with live reload"
	@echo "build - build docker image"
	GOTO :EOF

:build
	@docker build -t %IMAGE% .
	GOTO :EOF

:dev
	echo %PWD%
	@docker run --rm -v %PWD%:/app -p 127.0.0.1:8000:8000 -p 127.0.0.1:8001:8001 -it %IMAGE% adev runserver --livereload --host localhost --port 8000 run.py
	GOTO :EOF

:run
	@docker run --rm %IMAGE% -it -p 127.0.0.1:8000:8000 %IMAGE%
	GOTO :EOF

:test
	@docker run --rm -v %PWD%:/app -ti %IMAGE% python -m pytest --disable-warnings -v
	GOTO :EOF

:flake8
	@docker run --rm -v %PWD%:/app -ti %IMAGE% python -m flake8 lib
	GOTO :EOF

:pycodestyle
	@docker run --rm -v %PWD%:/app -ti %IMAGE% python -m pycodestyle lib
	GOTO :EOF

:pylint
	@docker run --rm -v %PWD%:/app -ti %IMAGE% python -m pylint lib
	GOTO :EOF

:lint
	CALL make.bat flake8
	CALL make.bat pycodestyle
	CALL make.bat pylint
	GOTO :EOF

:error
    IF "%1"=="" (
        ECHO make: *** No targets specified and no makefile found.  Stop.
    ) ELSE (
        ECHO make: *** No rule to make target '%1%'. Stop.
    )
    GOTO :EOF
