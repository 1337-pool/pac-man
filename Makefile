
install:
	uv sync
	pip install mazegenerator-00001-py3-none-any.whl --break-system-packages pygame


lint:
	-flake8 pac-man.py src/
	mypy pac-man.py src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	-flake8 pac-man.py src/
	mypy src pac-man.py --strict

