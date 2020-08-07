# The Basic SIR Model
#### This serves as a basic overview of how the epi-spot library works.

Refer to `tests/basic-sir-model.py` for the 
complementary code to this tutorial.
<br><br>

## Importing
Let's begin by importing `epispot`. If you've installed 
it from the pip, then just use `import epispot`. 
Otherwise, import from the file that you have cloned 
the library to, as shown in the example.

1. Installed from pip
    2. Use `import epispot`
2. Cloned from GitHub
    3. Use `from DIRECTORY-NAME import epispot`

## Parameters
Before we dive into creating the `Model`, we need to 
establish some of the parameters that will be used to 
define out model.
<br><br>
**Note: if you aren't sure about which parameters are 
needed for a specific model, always consult the 
compartment docstrings using the built-in Python 
`help()` command.**
<br><br>
Back to tutorial ...