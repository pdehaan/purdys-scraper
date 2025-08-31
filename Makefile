build:
		uv run main.py

lint:
		uvx ruff check
		uvx ty check
		uv run mypy *.py

format: lint
		uvx ruff format

diff:
		diff `ls -1 data/*.json | tail -2`
