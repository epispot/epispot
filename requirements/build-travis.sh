#!/bin/bash

# from root
cd ..

# create venv
python -m venv epispot-testing
source epispot-testing/bin/activate

# from requirements/
cd requirements
pip install -r requirements.txt
pip install -r requirements-nightly.txt
pip install -r requirements-dev.txt

# exit
cd ..
echo 'Requirements successfully installed; exited with 0'
exit 0
