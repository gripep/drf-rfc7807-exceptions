.PHONY : help test install

help:
# magic/stupid trick that looks for targets that have ## after the target, then prints it
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

format:  ## Run formatters (black, isort) with poetry
	poetry run isort drf_problem_detail_exceptions test_project
	poetry run black drf_problem_detail_exceptions test_project

install:  ## Install dependencies with poetry
	poetry install -v

shell:  ## Run poetry shell
	poetry shell

test-pytest:  ## Run pytest with poetry
	poetry run pytest test_project

test-tox:  ## Run tox
	tox
