.PHONY: install test lint format check clean docs serve monitor benchmark deploy help container db env perf venv

# Default target
all: install

# Create virtual environment
venv:
	test -d .venv || python3 -m venv .venv
	@echo "Virtual environment created at .venv"
	@echo "Activate with: source .venv/bin/activate"

# Show help (default target)
help:
	@echo "Available commands:"
	@echo "  make venv          - Create virtual environment"
	@echo "  make activate     - Activate virtual environment"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make install-prod - Install production dependencies"
	@echo "  make install-test - Install test dependencies"
	@echo "  make install-all  - Install all dependencies"
	@echo "  make install-env  - Install specific environment dependencies"
	@echo "  make format       - Format code"
	@echo "  make lint         - Run linters"
	@echo "  make style-check  - Run style checks"
	@echo "  make security-scan - Run security scan"
	@echo "  make test         - Run tests with coverage"
	@echo "  make perf-test    - Run performance tests"
	@echo "  make load-test    - Run load tests"
	@echo "  make docs         - Generate documentation"
	@echo "  make serve        - Start web server"
	@echo "  make monitor      - Run monitoring system"
	@echo "  make benchmark    - Run benchmarks"
	@echo "  make migrate      - Run database migration"
	@echo "  make db-downgrade - Downgrade database"
	@echo "  make db-create    - Create database"
	@echo "  make db-drop      - Drop database"
	@echo "  make db-init      - Initialize database"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make clean-venv   - Clean virtual environment"
	@echo "  make clean-db     - Clean database"
	@echo "  make clean-cache  - Clean cache"
	@echo "  make clean-logs   - Clean logs"
	@echo "  make update-venv  - Update virtual environment"
	@echo "  make venv-status  - Show virtual environment status"
	@echo ""
	@echo "To run a specific command, use: make [command]"
	@echo "For example: make install-dev"
	@echo ""
	@echo "To install specific environment dependencies, use: make install-env ENV=[env]"
	@echo "Where [env] can be 'dev', 'test', or 'prod'"

# Activate virtual environment
activate:
	@echo "Activating virtual environment..."
	@echo "Run 'source .venv/bin/activate' in your shell"

# Install development dependencies
install-dev:
	$(MAKE) venv
	@echo "Installing development dependencies..."
	.venv/bin/pip install -e .
	.venv/bin/pip install -r requirements-dev.txt

# Install production dependencies
install-prod:
	$(MAKE) venv
	@echo "Installing production dependencies..."
	.venv/bin/pip install -r requirements.txt

# Install test dependencies
install-test:
	$(MAKE) venv
	@echo "Installing test dependencies..."
	.venv/bin/pip install -r requirements-test.txt

# Install all dependencies
install-all:
	$(MAKE) install-dev
	$(MAKE) install-prod
	$(MAKE) install-test

# Install specific environment
install-env:
	ifneq "$(ENV)" ""
		$(MAKE) venv
		@echo "Installing environment dependencies for $(ENV)..."
		.venv/bin/pip install -r requirements-$(ENV).txt
	endif

# Format code
.PHONY: format
format:
	$(MAKE) install-dev
	@echo "Formatting code..."
	.venv/bin/isort .
	.venv/bin/black .

# Lint code
.PHONY: lint
lint:
	$(MAKE) install-dev
	@echo "Running linters..."
	.venv/bin/flake8 .
	.venv/bin/mypy .
	.venv/bin/isort --check-only .
	.venv/bin/black --check .

# Style check
.PHONY: style-check
style-check:
	$(MAKE) install-dev
	@echo "Running style checks on project code..."
	@echo "Checking code style..."
	.venv/bin/pycodestyle --max-line-length=100 --ignore=E501,E402 modules/**/*.py distributed/**/*.py monitoring/**/*.py notifications/**/*.py visualization/**/*.py web/**/*.py
	@echo "Checking docstrings..."
	.venv/bin/pydocstyle --ignore=D100,D101,D102,D103,D104,D105,D106,D107 modules/**/*.py distributed/**/*.py monitoring/**/*.py notifications/**/*.py visualization/**/*.py web/**/*.py
	@echo "Checking imports..."
	.venv/bin/isort --check-only --diff modules/**/*.py distributed/**/*.py monitoring/**/*.py notifications/**/*.py visualization/**/*.py web/**/*.py
	@echo "Checking black formatting..."
	.venv/bin/black --check --diff modules/**/*.py distributed/**/*.py monitoring/**/*.py notifications/**/*.py visualization/**/*.py web/**/*.py

# Security scan
.PHONY: security-scan
security-scan:
	$(MAKE) install-dev
	@echo "Running security scan..."
	.venv/bin/safety check
	.venv/bin/bandit -r .

# Run tests with coverage
.PHONY: test
test:
	$(MAKE) install-dev
	@echo "Running tests with coverage..."
	.venv/bin/pytest --cov=. --cov-report=term-missing

# Run performance tests
.PHONY: perf-test
perf-test:
	$(MAKE) install-dev
	@echo "Running performance tests..."
	.venv/bin/python -m benchmarks.performance

# Run load tests
.PHONY: load-test
load-test:
	$(MAKE) install-dev
	@echo "Running load tests..."
	.venv/bin/locust -f tests/load_test.py

# Generate documentation
.PHONY: docs
docs:
	$(MAKE) install-dev
	@echo "Generating documentation..."
	.venv/bin/pip install -r requirements-dev.txt
	.venv/bin/pip install sphinx sphinx-rtd-theme
	sphinx-apidoc -o docs/ src/
	cd docs && make html

# Start web server
.PHONY: serve
serve:
	$(MAKE) install-dev
	@echo "Starting web server..."
	.venv/bin/python -m web.app

# Run monitoring system
.PHONY: monitor
monitor:
	$(MAKE) install-dev
	@echo "Starting monitoring system..."
	.venv/bin/python -m monitoring.monitor

# Run benchmarks
.PHONY: benchmark
benchmark:
	$(MAKE) install-dev
	@echo "Running benchmarks..."
	.venv/bin/python -m benchmarks.benchmark

# Run database migrations
.PHONY: migrate
db-migrate:
	$(MAKE) install-dev
	@echo "Running database migration..."
	.venv/bin/python -m alembic upgrade head

# Run database downgrade
.PHONY: db-downgrade
db-downgrade:
	$(MAKE) install-dev
	@echo "Running database downgrade..."
	.venv/bin/python -m alembic downgrade -1

# Create database
.PHONY: db-create
db-create:
	$(MAKE) install-dev
	@echo "Creating database..."
	.venv/bin/python -m alembic upgrade base

# Drop database
.PHONY: db-drop
db-drop:
	$(MAKE) install-dev
	@echo "Dropping database..."
	.venv/bin/python -m alembic downgrade base

# Initialize database
.PHONY: db-init
db-init:
	$(MAKE) install-dev
	@echo "Initializing database..."
	.venv/bin/python -m database.init

# Clean build artifacts
.PHONY: clean
clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf .docker

# Clean virtual environment
.PHONY: clean-venv
clean-venv:
	rm -rf .venv
	rm -rf .venv-version

# Clean database
.PHONY: clean-db
clean-db:
	dropdb ai_masterclass
	createdb ai_masterclass

# Clean cache
.PHONY: clean-cache
clean-cache:
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache

# Clean logs
.PHONY: clean-logs
clean-logs:
	rm -rf logs/*.log

# Update virtual environment
.PHONY: update-venv
update-venv:
	$(MAKE) clean-venv
	$(MAKE) venv
	$(MAKE) install-dev
	$(MAKE) install-prod
	$(MAKE) install-env ENV=dev
	$(MAKE) install-env ENV=test
	$(MAKE) install-env ENV=prod

# Show virtual environment status
.PHONY: venv-status
venv-status:
	@echo "Virtual environment status:"
	@echo "Location: .venv"
	@echo "Python version: $(shell .venv/bin/python --version)"
	@echo "Packages: $(shell .venv/bin/pip list)"

# Show help
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make venv          - Create virtual environment"
	@echo "  make activate     - Activate virtual environment"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make install-prod - Install production dependencies"
	@echo "  make install-test - Install test dependencies"
	@echo "  make install-all  - Install all dependencies"
	@echo "  make install-env  - Install specific environment dependencies"
	@echo "  make format       - Format code"
	@echo "  make lint         - Run linters"
	@echo "  make style-check  - Run style checks"
	@echo "  make security-scan - Run security scan"
	@echo "  make test         - Run tests with coverage"
	@echo "  make perf-test    - Run performance tests"
	@echo "  make load-test    - Run load tests"
	@echo "  make docs         - Generate documentation"
	@echo "  make serve        - Start web server"
	@echo "  make monitor      - Run monitoring system"
	@echo "  make benchmark    - Run benchmarks"
	@echo "  make migrate      - Run database migration"
	@echo "  make db-downgrade - Downgrade database"
	@echo "  make db-create    - Create database"
	@echo "  make db-drop      - Drop database"
	@echo "  make db-init      - Initialize database"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make clean-venv   - Clean virtual environment"
	@echo "  make clean-db     - Clean database"
	@echo "  make clean-cache  - Clean cache"
	@echo "  make clean-logs   - Clean logs"
	@echo "  make update-venv  - Update virtual environment"
	@echo "  make venv-status  - Show virtual environment status"

# Clean virtual environment
clean-venv:
	rm -rf .venv
	rm -rf .venv-version

# Update virtual environment
update-venv:
	$(MAKE) clean-venv
	$(MAKE) venv
	$(MAKE) install
	$(MAKE) install-prod
	$(MAKE) install-env ENV=dev
	$(MAKE) install-env ENV=test
	$(MAKE) install-env ENV=prod

# Show virtual environment status
venv-status:
	@echo "Virtual environment status:"
	@echo "Location: .venv"
	@echo "Python version: $(shell .venv/bin/python --version)"
	@echo "Packages: $(shell .venv/bin/pip list)"

# Run tests with coverage
.PHONY: test
test:
	$(MAKE) install-dev
	PYTHONPATH=$(CURDIR) .venv/bin/pytest --cov=. --cov-report=term-missing

# Run tests with coverage and HTML report
test-html:
	pytest --cov=. --cov-report=html

# Run performance tests
perf-test:
	$(MAKE) install-dev
	@echo "Running performance tests..."
	.venv/bin/python -m benchmarks.performance

# Run load tests
load-test:
	$(MAKE) install-dev
	@echo "Running load tests..."
	.venv/bin/locust -f tests/load_test.py

# Run security scan
.PHONY: security-scan
security-scan:
	$(MAKE) install-dev
	@echo "Running security scan..."
	.venv/bin/safety check
	.venv/bin/bandit -r .

# Run style checks
.PHONY: style-check
style-check:
	$(MAKE) install-dev
	@echo "Running style checks..."
	.venv/bin/pycodestyle .
	.venv/bin/pydocstyle .

# Run load tests
load-test:
	$(MAKE) venv
	@echo "Running load tests..."
	.venv/bin/locust -f tests/load_test.py

# Run linters
.PHONY: lint
lint:
	$(MAKE) venv
	@echo "Running linters..."
	.venv/bin/flake8 .
	.venv/bin/mypy .
	.venv/bin/isort --check-only .
	.venv/bin/black --check .

# Format code
.PHONY: format
format:
	$(MAKE) install-dev
	@echo "Formatting code..."
	.venv/bin/isort .
	.venv/bin/black .

# Lint code
.PHONY: lint
lint:
	$(MAKE) install-dev
	@echo "Running linters..."
	.venv/bin/flake8 .
	.venv/bin/mypy .
	.venv/bin/isort --check-only .
	.venv/bin/black --check .

# Run tests with coverage
.PHONY: test
test:
	$(MAKE) install-dev
	@echo "Running tests with coverage..."
	.venv/bin/pytest --cov=. --cov-report=term-missing

# Clean build artifacts
.PHONY: clean
clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf .docker

# Clean database
.PHONY: clean-db
clean-db:
	dropdb ai_masterclass
	createdb ai_masterclass

# Clean cache
.PHONY: clean-cache
clean-cache:
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache

# Clean logs
.PHONY: clean-logs
clean-logs:
	rm -rf logs/*.log

# Generate documentation
docs:
	$(MAKE) venv
	@echo "Generating documentation..."
	.venv/bin/pip install -r requirements-dev.txt
	.venv/bin/pip install sphinx sphinx-rtd-theme
	sphinx-apidoc -o docs/ src/
	cd docs && make html

# Start web server
.PHONY: serve
serve:
	$(MAKE) venv
	@echo "Starting web server..."
	.venv/bin/python -m web.app

# Run monitoring system
.PHONY: monitor
monitor:
	$(MAKE) venv
	@echo "Starting monitoring system..."
	.venv/bin/python -m monitoring.monitor

# Run benchmarks
.PHONY: benchmark
benchmark:
	$(MAKE) venv
	@echo "Running benchmarks..."
	.venv/bin/python -m benchmarks.benchmark

# Run database migrations
.PHONY: migrate
db-migrate:
	$(MAKE) venv
	@echo "Running database migration..."
	.venv/bin/python -m alembic upgrade head

# Run database downgrade
.PHONY: db-downgrade
db-downgrade:
	$(MAKE) venv
	@echo "Running database downgrade..."
	.venv/bin/python -m alembic downgrade -1

# Create database
.PHONY: db-create
db-create:
	$(MAKE) venv
	@echo "Creating database..."
	.venv/bin/python -m alembic upgrade base

# Drop database
.PHONY: db-drop
db-drop:
	$(MAKE) venv
	@echo "Dropping database..."
	.venv/bin/python -m alembic downgrade base

# Initialize database
.PHONY: db-init
db-init:
	$(MAKE) venv
	@echo "Initializing database..."
	.venv/bin/python -m database.init

# Backup database
.PHONY: db-backup
db-backup:
	pg_dump ai_masterclass > backups/$(shell date +%Y%m%d_%H%M%S).sql

# Restore database
.PHONY: db-restore
db-restore:
	ifneq "$(BACKUP_FILE)" ""
		pg_restore -d ai_masterclass $(BACKUP_FILE)
	endif

# Build container
.PHONY: container-build
container-build:
	docker build -t bosskit .

# Run container
.PHONY: container-run
container-run:
	docker run -p 8000:8000 -v $(PWD):/app bosskit

# Stop container
.PHONY: container-stop
container-stop:
	docker stop bosskit
	docker rm bosskit

# Clean containers
.PHONY: container-clean
container-clean:
	docker stop $(docker ps -a -q)
	docker rm $(docker ps -a -q)
	docker rmi bosskit

# Run all checks
.PHONY: check
check:
	$(MAKE) lint
	$(MAKE) test

# Run security scan
.PHONY: security-scan
security-scan:
	safety check
	bandit -r .

# Run style checks
.PHONY: style-check
style-check:
	pycodestyle .
	pydocstyle .

# Build and deploy
.PHONY: deploy
deploy:
	$(MAKE) clean
	$(MAKE) test
	$(MAKE) lint
	$(MAKE) container-build
	docker push bosskit:latest

# Show help
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install          - Install development dependencies"
	@echo "  make install-prod    - Install production dependencies"
	@echo "  make install-env     - Install specific environment dependencies"
	@echo "  make test            - Run tests with coverage"
	@echo "  make test-html       - Run tests with HTML coverage report"
	@echo "  make perf-test       - Run performance tests"
	@echo "  make load-test       - Run load tests"
	@echo "  make lint            - Run code linters"
	@echo "  make format          - Format code"
	@echo "  make clean           - Clean build artifacts"
	@echo "  make clean-db        - Clean database"
	@echo "  make clean-cache     - Clean cache"
	@echo "  make clean-logs      - Clean logs"
	@echo "  make docs            - Generate documentation"
	@echo "  make serve           - Start web server"
	@echo "  make monitor         - Run monitoring system"
	@echo "  make benchmark       - Run benchmarks"
	@echo "  make check           - Run all checks"
	@echo "  make security-scan   - Run security scans"
	@echo "  make style-check     - Run style checks"
	@echo "  make deploy          - Build and deploy application"
	@echo "  make container-build - Build Docker container"
	@echo "  make container-run   - Run Docker container"
	@echo "  make container-stop  - Stop Docker container"
	@echo "  make container-clean - Clean Docker containers"
	@echo "  make db-migrate      - Run database migrations"
	@echo "  make db-downgrade    - Downgrade database"
	@echo "  make db-create       - Create database"
	@echo "  make db-drop         - Drop database"
	@echo "  make db-init         - Initialize database"
	@echo "  make db-backup       - Backup database"
	@echo "  make db-restore      - Restore database"
