echo "Creating conda env `epispot`..."
conda create -n epispot
echo "Activating env..."
conda activate epispot
echo "Completed!"
echo "Installing requirements with `pip`..."
pip install -r requirements/requirements-dev.txt
echo "Completed!"
echo "Installation complete."
