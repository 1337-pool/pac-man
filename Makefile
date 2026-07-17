

run:
	uv run python3 pac-man.py config.json

install:
	uv sync
	UV_SKIP_WHEEL_FILENAME_CHECK=1 uv pip install mazegenerator-00001-py3-none-any.whl pygame

lint:
	-flake8 pac-man.py src/
	mypy pac-man.py src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	-flake8 pac-man.py src/
	mypy src pac-man.py --strict

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .mypy_cache

debug:
	uv run python3 -m pdb pac-man.py config.json