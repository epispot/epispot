# CI Testing Suite
To run all tests, first install all dependencies:
```shell
$ pip install -r requirements.txt  # conda install -r requirements.txt
$ pip install pytest  # conda install pytest
```
Or their `conda` equivalents in the comments. Then, navigate to the root directory 
(this is important--or there will be an `ImportError` when installing `epispot`) and 
build the nightly version of epispot from the source with:
```shell
$ cd ROOT  # replace with root directory
$ python develop setup-nightly.py  # conda develop setup-nightly.py
```
Now, you can initiate `pytest`. Run it as a Python module so that Python correctly 
imports the `epispot` directory. Note that any test in the form `test_x` is a base test 
that tests basic package or module information. To run tests use:
```shell
$ python -m pytest
```
Run with the `--ignore` flag (shown below) to suppress certain test results while 
developing or to speed up tests by only running relevant tests.
```shell
$ python -m pytest --ignore=dir  # replace with directories to ignore
```
You can also run a specific file using `pytest` with:
```shell
$ python -m pytest test_foo.py  # replace with file to run
```