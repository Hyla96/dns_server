setup: |
	uv venv --python 3.12
	make install
	pre-commit install

install:
	uv pip install -r requirements.txt -r requirements_dev.txt

generate_requirements:
	uv pip compile requirements.in -o requirements.txt

generate_requirements_dev:
	uv pip compile requirements_dev.in -o requirements_dev.txt

format:
	ruff format

lint:
	ruff check --fix