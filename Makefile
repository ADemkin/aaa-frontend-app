download:
	@python -c "from lib.models import get_model; get_model()" 1>/dev/null

test:
	@pytest -v

fmt:
	@ruff check --fix lib tests
	@ruff format lib tests

lint:
	@ruff check lib tests

dev:
	@fastapi dev lib/app.py
