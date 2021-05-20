# testing-examples
**This directory contains epispot's old testing and CI suite; these tests are not 
compatible with newer versions of epispot**
---

This directory contains all the testing files that are executed in 
.github/workflows, however, many of these files may not work if run locally. 
This is because some files contain path references which will only be valid if 
executed from a certain root directory--to see the latest tests **do not** run 
the files locally but rather look at the latest GitHub build.