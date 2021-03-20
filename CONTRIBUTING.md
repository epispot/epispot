# Contributing Guidelines
Thank you for contributing to the epispot repo! Here are some guidelines to streamline all contributions so we can accept issues and/or pull requests as fast as possible.
## Issues
### I found a bug.
When creating an issue, you will be prompted to choose a template. Choose `BUG_REPORT` and fill in the required information before submitting the issue.
### I have a feature requeset.
When creating the issue, you will also be prompted to choose a template. Choose `FEATURE_REQUEST` and fill out the template with any information that you have.
### I found a security vulnerability.
Check out the steps outlined in [SECURITY.md](SECURITY.md) and submit the issue after verifying that the vulnerability still exists on a supported version.
### Neither.
Cool! Create a blank issue and give us as much information as possible to make fixing your issue as easy as possible. 
It is also good to add labels to your issue to increase its visibility to other contributors and to help maintainers understand its impact to the overall project.
## Pull Requests
### Development Structure
Before creating your PR, understand which branch to work on in the first place.
The **master** branch is mainly only for critical issues since all new feature and developments pass through the **nightly** branch first as a testing ground before being 
merged into the final package.
| Purpose | Branch |
| --- | --- |
| Fixes a *critical* bug | **master** |
| Fixes an issue tagged with **help wanted** | **master** |
| Fixes an issue tagged with **high-priority** | **master** |
| Maintenance on the main package | **master** |
| Documentation improvements | **master** |
| Adds a new feature (specified or unspecified by an issue) | **nightly** |
| General code cleanup | **nightly** |
| Fixes an issue tagged with **nightly** | **nightly** |
| Maintenance on the nightly package | **nightly** |
### Tests
When you first create your PR, an array of tests will be triggered to run. Don't worry! Here's a guide to what each test does and what its status means:
| Test | Passing | Failing |
| -- | --- | --- |
| Code Coverage | You've increased our testing capacity! | You may have added a new feature without providing testing scripts. |
| Build 3.7 | All code is working on Python 3.7 | Code is incompatible with Python 3.7 |
| Build 3.8 | All code is working on Python 3.8 | Code is incompatible with Python 3.8 |
| Build 3.9 | All code is working on Python 3.9 | Code is incompatible with Python 3.9 |
| CodeFactor | Wow! No new code alerts! | Your new code may introduce minor maintainability issues |
| Codecov | Code coverage metrics were successfully uploaded | Problem with uploading code coverage metrics |

Don't worry if one (or even two) tests fail! Your PR is still useful, but there might still be things to improve on. We'll discuss this when your PR is reviewed.
### Priority
Pull requests are prioritized by the following criteria:
 - Branch
    1. master
    2. nightly
    3. other branches
 - Tests
    1. Build 3.7
    2. Build 3.8
    3. Build 3.9
    4. Codecov
    5. Code Coverage
    6. CodeFactor
 - Tags
    1. high-priority
    2. help-wanted
    3. other tags
    4. low-priority
 - Code Review
    1. More than 1 code review with pending code review
    2. More than 1 code review
    3. 1 code review with pending code review
    4. 1 code review
    5. Pending code review
    6. No code reviews
