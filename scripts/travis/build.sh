echo "Installing dependencies..."
pip install pandas
pip install matplotlib~=3.4.2
sudo apt-get install dvipng texlive-latex-extra texlive-fonts-recommended cm-super  # install LaTeX requirements for Travis CI
pip install -r requirements/requirements-dev.txt
echo "Finished installing dependencies."