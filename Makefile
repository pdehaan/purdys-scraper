build:
		uv run main.py

lint:
		uvx ruff check
		uvx ty check

format: lint
		uvx ruff format
