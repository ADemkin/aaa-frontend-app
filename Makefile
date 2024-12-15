download:
	@python -c "from lib.models import get_model; get_model()"

test:
	@pytest -v

fmt:
	@ruff format lib tests

lint: fmt
	@ruff check --fix lib tests

dev:
	@fastapi dev lib/app.py
