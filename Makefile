.DEFAULT_GOAL:= build
SHELL := /bin/bash
VENV ?= "$(shell poetry env list --full-path | cut -f1 -d " ")/bin/activate"

# Releasing
tag:
	@git tag -a $(version) -m "Release $(version) -> Jenkins TUI"
	@git push --follow-tags

# Building
build: check
	@source $(VENV)
	python tools/bump_version.py
	rm -rf dist || true
	@poetry build

check:
	@source $(VENV)
	black --check .
	mypy tools
	isort --check src/jenkins_tui
	mypy src/jenkins_tui
	darglint -m "{path}:{line} -> {msg_id}: {msg}" src/jenkins_tui

# Developing
.PHONY: init
init:
	@poetry install
	@pre-commit install
