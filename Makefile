# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gtourdia & lbonnet <@student.42mulhouse.fr>+#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#                                                      #+#    #+#              #
#    26/01/2026            A Maze Ing                 ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


# PROJECT CONFIGURATION
AUTHOR=gtourdia & lbonnet
PROJECT_NAME=A-Maze-Ing
PROJECT_START_DATE=2026-02-23
GITHUB=https://github.com/sousampere/42_a_maze_ing

# COLORS
YELLOW=\033[0;33m
CYAN=\033[0;36m
GREEN=\033[0;32m
RESET=\033[0m

# MAIN VARIABLES
INTERPRETER			=	python3


install:
	@echo "$(YELLOW)╔════════════════════════════════════════════════════════════════╗"
	@echo "$(YELLOW)║                                                                ║"
	@echo "$(YELLOW)║  44  44    2222    $(GREEN)Made with ♥ by $(AUTHOR) $(YELLOW)          ║"
	@echo "$(YELLOW)║  44  44   22  22   Project: $(CYAN)$(PROJECT_NAME) $(YELLOW)                        ║"
	@echo "$(YELLOW)║  444444      22    Started in: $(CYAN)$(PROJECT_START_DATE) $(YELLOW)                     ║"
	@echo "$(YELLOW)║      44     22                                                 ║"
	@echo "$(YELLOW)║      44   222222                                               ║"
	@echo "$(YELLOW)║                                                                ║"
	@echo "$(YELLOW)╚════════════════════════════════════════════════════════════════╝"
	@echo
	@echo "$(CYAN)[Installation]$(RESET) ➡️  Synchronizing uv"
	uv sync

sync:
	uv sync


# ---------------- A VERIFIER -------------------

run:
	uv run python a_maze_ing_test.py config.txt

flake8: sync
	uv run python -m flake8 ./src

mypy: sync
	uv run python -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

mypy-strict: sync
	uv run python -m mypy . --strict

lint: flake8 mypy

lint-strict: flake8 mypy-strict

clean:
	echo WIP

re: clean install
	echo WIP

build:
	rm -rf dist
	uv build