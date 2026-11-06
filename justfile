# Check for formatting issues
lint:
	ruff format . --check
	ruff check .

# Fix formatting issues (where possible)
format:
	ruff format .
	ruff check . --fix --show-fixes

# Run tests
test:
	pytest --benchmark-skip

# Run benchmark tests
bench:
	pytest --benchmark-only

# Generate test coverage report
coverage:
	coverage run -m pytest --benchmark-skip
	coverage html

# Build wheel package
build:
	uv build
