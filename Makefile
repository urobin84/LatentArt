# Project LatentArt Makefile

VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
JUPYTER = $(VENV)/bin/jupyter
NOTEBOOK = notebooks/LatentArt_Submission.ipynb

.PHONY: setup run clean help

help:
	@echo "Available commands:"
	@echo "  make setup    - Create virtual environment and install dependencies"
	@echo "  make run      - Execute the submission notebook in-place"
	@echo "  make clean    - Remove virtual environment and outputs"

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install nbconvert jupyter

run:
	@echo "Executing notebook: $(NOTEBOOK)..."
	$(JUPYTER) nbconvert --to notebook --execute --inplace $(NOTEBOOK)
	@echo "Execution complete. Check the 'outputs/' directory for results."

streamlit:
$(PYTHON) -m streamlit run src/app.py

clean:
	rm -rf $(VENV)
	rm -rf outputs/*.png
	@echo "Cleanup complete."
