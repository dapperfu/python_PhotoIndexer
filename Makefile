## Setup
# Python VER
VER=3.8


# Paths
PROJ_DIR:=$(realpath $(dir $(firstword ${MAKEFILE_LIST})))
PROJ?=$(notdir ${PROJ_DIR})
VENV?=venv${VER}
BIN=$(abspath ${VENV}/bin)
PYTHON=${BIN}/python${VER}


# Debug Variables
.PHONY: debug
debug:
	$(info $${PROJ_DIR}=${PROJ_DIR})
	$(info $${PROJ}=${PROJ})
	$(info $${BIN}=${BIN})
	$(info $${PYTHON}=${PYTHON})
	
## Environment
# Create virtual environment.
.PHONY: venv
venv: ${VENV}
${VENV}:
	@python3.8 -mvenv ${@}
	@${BIN}/pip install --upgrade pip setuptools wheel
	@${MAKE} requirements
	
# Install requirements
.PHONY: requirements
requirements: requirements.txt
	@${BIN}/pip install --upgrade --requirement requirements.txt
	@${BIN}/pip install --editable .

# Conda environment
.PHONY: conda.env
cenv: environment.yml
	conda env create -f ${^}
	
# Generate Conda Environment file.
environment.yml:
	conda env export --from-history | grep -v "^prefix: " > ${@}

## Action Targets
# Notebook in a screen.
.PHONY:notebook
notebook:
	screen -S ${PROJ} -d -m jupyter-notebook

# Notebook locally in a screen.
.PHONY: lab
lab:
	screen -S ${PROJ} -d -m jupyter-lab

# Launch a worker.
.PHONY:worker
worker:
	screen -S ${PYTHON} worker.py

# Launch 8 workers in a screen.
.PHONY:worker8
worker8:
	screen -AdmS ${PROJ} -t worker0 ${PYTHON} worker.py
	screen -S ${PROJ} -X screen -t worker1 ${PYTHON} worker.py
	screen -S ${PROJ} -X screen -t worker2 ${PYTHON} worker.py
	screen -S ${PROJ} -X screen -t worker3 ${PYTHON} worker.py
	screen -S ${PROJ} -X screen -t worker4 ${PYTHON} worker.py
	screen -S ${PROJ} -X screen -t worker5 ${PYTHON} worker.py
	screen -S ${PROJ} -X screen -t worker6 ${PYTHON} worker.py
	screen -S ${PROJ} -X screen -t worker7 ${PYTHON} worker.py
## Make Documentation
# Generate the README from the Jupyter Notebook.
README.md: README.ipynb
	jupyter-nbconvert --ExecutePreprocessor.timeout=600 --execute --to markdown --output=${@} ${<}


.PHONY: clean.docs
clean.docs:
	rm -rf docs scripts
# Convert Notebooks to other formats.
IPYNB:=$(wildcard *.ipynb)
PY:=$(patsubst %.ipynb,scripts/%.py,${IPYNB})
MD:=$(patsubst %.ipynb,docs/markdown/%.md,${IPYNB})
PDF:=$(patsubst %.ipynb,docs/pdf/%.pdf,${IPYNB})
HTML:=$(patsubst %.ipynb,docs/html/%.html,${IPYNB})
.PHONY: docs
docs: ${MD} ${PDF} ${HTML} ${PY}

scripts/%.py: %.ipynb
	mkdir -p `dirname ${@}`
	${BIN}/jupyter-nbconvert --ExecutePreprocessor.timeout=600 --execute --to python --output=${@} ${<}

docs/markdown/%.md: %.ipynb
	mkdir -p `dirname ${@}`
	jupyter-nbconvert --ExecutePreprocessor.timeout=600 --execute --to markdown --output=${@} ${<}

docs/pdf/%.pdf: %.ipynb
	mkdir -p `dirname ${@}`
	jupyter-nbconvert --ExecutePreprocessor.timeout=600 --execute --to pdf --output=${@} ${<}

docs/html/%.html: %.ipynb
	mkdir -p `dirname ${@}`
	jupyter-nbconvert --ExecutePreprocessor.timeout=600 --execute --to html --output=${@} ${<}
