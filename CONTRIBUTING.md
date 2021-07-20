# Contributing Guidelines
Thank you for contributing to the epispot repo! Here are some guidelines to streamline all contributions so we can accept issues and/or pull requests as fast as possible.

**Important Note:**
> If you are working on a documentation patch, please see
> [DOCUMENTATION.md](DOCUMENTATION.md) for more information.
> For security patches, see [SECURITY.md](SECURITY.md).

## Issues
### I found a bug.
When creating an issue, you will be prompted to choose a template. Choose `BUG_REPORT` and fill in the required information before submitting the issue.
### I have a feature request.
When creating the issue, you will also be prompted to choose a template. Choose `FEATURE_REQUEST` and fill out the template with any information that you have.
### I found a security vulnerability.
Check out the steps outlined in [SECURITY.md](SECURITY.md) and submit the issue after verifying that the vulnerability still exists on a supported version.
### Neither.
Cool! Create a blank issue and give us as much information as possible to make fixing your issue as easy as possible.
It is also good to add labels to your issue to increase its visibility to other contributors and to help maintainers understand its impact to the overall project.
## Pull Requests

No matter what kind of PR you'll submit, first make sure you do the following:
1. Fork the repo
2. Clone your fork
3. Run the build script:
   ```sh
   bash scripts/build.sh
   ```
4. Follow the steps listed below for the type of PR you'll be submitting.
### Tests
When you first create your PR, an array of tests will be triggered to run.
Here's a guide to what each test does and what its status means:

| Test | Status Passing | Status Failing |
| --- | --- | --- |
| CodeQL / Analyze | No new vulnerabilities introduced | Security vulnerability detected |
| LGTM analysis: Python | No major code quality issues | Possible code quality issues |
| DeepSource: Python | No technical debt | Possible technical debt introduced |
| Travis CI | Build passed | Build failed |
| codecov/patch | Patch code coverage good | Patch code coverage bad |
| codecov/project | Code coverage increased | Code coverage decreased |
### Priority
Pull requests are prioritized by the following criteria:
 1. Branch
    1. master
    2. other branches
 2. Tests
    1. CodeQL
    2. Travis CI
    3. LGTM
    3. CodeCov Project
    4. DeepSource
 3. Tags
    1. high-priority
    2. help-wanted
    3. low-priority
    4. untagged
 4. Code Review
    1. More than 1 code review with pending code review
    2. More than 1 code review
    3. 1 code review with pending code review
    4. 1 code review
    5. Pending code review
    6. No code reviews
