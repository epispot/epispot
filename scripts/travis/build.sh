echo "Installing dependencies..."
pip install -r requirements/requirements-dev.txt
sudo apt-get install dvipng texlive-latex-extra texlive-fonts-recommended cm-super  # install LaTeX requirements for Travis CI
pip install -r requirements/requirements-travis.txt
echo "Finished installing dependencies."