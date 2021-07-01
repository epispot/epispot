echo "Creating conda env..."
conda create -n epispot python=3.9
echo "Activating env..."
conda activate epispot
echo "Completed!"
echo "Installing requirements..."
pip install -r requirements/requirements-dev.txt
echo "Completed!"
echo "Your dev environment is completely set up. Install additional dependencies to the conda environment epipsot, and make sure to activate the env before you start to develop on the project."