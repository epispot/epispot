# Documentation
The docstring standard for epispot

## Basic Rules

Docstring format:
``` python
def function (parameters):
    """
    Overview
    - [PARAM NAME]: [DESCRIPTION]
      continued description\
      list intro:
        - a list item
        - more list items
    - [PARAM NAME]: [DESCRIPTION]
    ...
    """
    ...
```

**Make sure indentation is accurate.** \
**Use of ReST Directives such as:**
- **`..include::`**
- **`..math::`**
- **`..versionadded::`**
- **[and more](https://pdoc3.github.io/pdoc/doc/pdoc/#supported-rest-directives)** \
\
The directives such as `:param:` and `:returns` are not valid, however.

### LaTeX Math
Use of latex math is permitted. See [this](https://pdoc3.github.io/pdoc/doc/pdoc/#supported-docstring-formats) for more.
