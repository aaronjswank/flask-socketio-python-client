# Makefile Variables

# Name of the project
PROJ = test

# Directory to place the python virtual environment
VENV_DIR = ~/.venv/$(PROJ)

#
# Install Requirements via PIP
init:
	pip install -r requirements.txt

lint:
	pylint --disable=R,C */*.py

test: lint


# DEVELOPER:  Make Commands
	
# Make the Virtual Environment
venv:
	# TODO: Switch on PYTHON_VERSION
	# Python 3.6
	python3 -m venv $(VENV_DIR)
		
	# Python 3.4/3.5 with Broken PIP (Redhat 7)
	#python3 -m venv --without-pip $(VENV_DIR) && \
       	curl https://bootstrap.pypa.io/get-pip.py | \
       	$(VENV_DIR)/bin/python3

	@echo "You may now execute: source $(VENV_DIR)/bin/activate"
