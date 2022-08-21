# Documentation

The docstring standard for epispot

## Basic Rules

Docstring format (all sections should only be used if necessary):

```python
def function(parameters):
    """
    Overview/short description

    ## Function Parameters

    If the output of running this function is another function,
    provide usage information here in the same format as the "parameters" section.

    ## Parameters

    `parameters (type)`: description

    `another_parameter=default (type)`: very long description that has punctuation;
      thus, it is split across lines.
      Continuing lines are indented.

    ## Example

    Show an example with code here:

    ```python
    print('hello world')
    ```

    Describe the above code example.

    ## Usage

    If additional notes about how to use this function are required, put them here.
    Insert code snippets if necessary.

    ## Error Handling

    ### `ErrorType`

    Describe the situations under which this function will raise an error and why the error is raised.

    ### `AnotherErrorType`

    Do the same thing here.

    ## Additional Notes

    Sometimes, additional (more technical) nootes are required;
    put them here if that is the case.

    ## Returns

    Describe the return value of the function (`type`).

    """
    ...
```

**Make sure indentation is accurate.** \
**Use of ReST Directives are permitted, such as:**

- **`..include::`**
- **`..math::`**
- **`..versionadded::`**
- **[and more](https://pdoc3.github.io/pdoc/doc/pdoc/#supported-rest-directives)** \
\
The directives such as `:param:` and `:returns` are not valid, however.

### LaTeX Math

Use of LaTeX math is permitted. See [this](https://pdoc3.github.io/pdoc/doc/pdoc/#supported-docstring-formats) for more.

## Building Documentation

Epispot uses [`pdoc3`](https://www.github.com/pdoc3/pdoc) to build its documentation
automatically from docstrings. If you are interested in helping to expand epispot's
documentation, do *not* change the documentation source files in the
[`gh-pages`](https://www.github.com/epispot/epispot/tree/gh-pages) branch.
This branch is frequently overridden by automatic documentation from the latest build.
Rather, to help expand epispot's documentation, fork the
latest version of the repository and change the
docstrings in the source code. Next, build the docs with this command:

```shell
pdoc --html --output-dir docs epispot
```

Make sure that the output directory is `docs` so that after you push your changes, the
docs are hidden (because they are blocked via the `.gitignore`). As soon as your PR is
merged, the docs will be auto-generated and pushed to the
[`gh-pages`](https://www.github.com/epispot/epispot/tree/gh-pages) branch.
<br><br>
To delete the previous documentation, run:

```shell
pdoc --html --output-dir docs epispot --force
```
