import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="epispot",
    version="0.0.1",
    author="quantum9innovation",
    description="A tool for modelling infectious diseases.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quantum9innovation/epi-spot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
