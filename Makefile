.PHONY : help test install

help:
# magic/stupid trick that looks for targets that have ## after the target, then prints it
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

format:  ## Run formatters (black, isort) with poetry
	poetry run isort drf_rfc7807_exceptions test_project
	poetry run black drf_rfc7807_exceptions test_project

install:  ## Install dependencies with poetry
	poetry install -v

lint:  ## Check format (black, isort) and run flake8
	poetry run isort --check drf_rfc7807_exceptions test_project
	poetry run black --check drf_rfc7807_exceptions test_project --exclude migrations
	poetry run flake8 drf_rfc7807_exceptions test_project --max-line-length 88

shell:  ## Run poetry shell
	poetry shell

test:  ## Run pytest with poetry
	poetry run pytest test_project
