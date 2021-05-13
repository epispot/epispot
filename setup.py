import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="epispot",
    version="v2.1.1",
    author="quantum9innovation",
    description="A tool for modeling infectious diseases.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://epispot.github.io",
    project_urls={
        "Repository": "https://github.com/epispot/epispot",
        "Changelog": "https://github.com/epispot/epispot/tree/master/CHANGELOG.md",
        "Bug Tracker": "https://github.com/epispot/epispot/issues",
        "Documentation": "https://epispot.github.io/epispot",
        "Code Coverage": "https://app.codecov.io/gh/epispot/epispot"
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.6',
    install_requires=['matplotlib', 'numpy', ],
)

