.PHONY : help test install

help:
# magic/stupid trick that looks for targets that have ## after the target, then prints it
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

format:  ## Run formatters (black, isort)
	poetry run isort drf_problem_detail_exceptions test_project
	poetry run black drf_problem_detail_exceptions test_project

install:  ## Install dependencies
	poetry install -v

test-pytest:  ## Run pytest
	poetry run pytest test_project

test-tox:  ## Run tox
	tox
