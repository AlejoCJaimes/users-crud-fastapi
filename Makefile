# Create a makefile configuration for the project for launching the project using uvicorn and another for install dependencies
# Path: requirements.txt
VENV_DIR := venv
PYTHON := python3

.PHONY: help

help:
	@echo "Comandos de Makefile 📜"
	@echo "make help - Muestra esta ayuda 🆘"
	@echo "make build-dev - Crea un entorno virtual e instala las dependencias 🐍"
	@echo "make run-dev - Ejecuta el proyecto usando uvicorn ✅"
	@echo "make venv - Crea un entorno virtual 🐻"
	@echo "make activate - Activa el entorno virtual 🏏"
	@echo "make install - Instala las dependencias 📦"

venv:
	@echo "Creating virtual environment 🐍"
	$(PYTHON) -m venv $(VENV_DIR)

activate:
	@echo "Activating virtual environment 🐍"
	@. $(VENV_DIR)/bin/activate

install:
	@echo "Installing dependencies 📦"
	@pip install -r infraestructure/requirements.txt

build-dev: venv activate install

run-dev:
	@echo "Run the project using uvicorn ✅"
	@uvicorn app.main:app --port 8000 --reload