import setuptools

with open('README-nightly.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='epispot-nightly',
    version='3.0.0-alpha-3',
    author='quantum9innovation',
    author_email = 'dev.quantum9innovation@gmail.com',
    description='The nightly version of the epispot package.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://epispot.github.io',
    project_urls={
        'Repository': 'https://github.com/epispot/epispot',
        'Changelog': 'https://github.com/epispot/epispot/tree/master/CHANGELOG.md',
        'Bug Tracker': 'https://github.com/epispot/epispot/issues',
        'Documentation': 'https://epispot.github.io/epispot',
        'Code Coverage': 'https://app.codecov.io/gh/epispot/epispot'
    },
    packages=setuptools.find_packages('epispot/'),
    scripts=['bin/epispot'],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
    ],
    python_requires='>=3.7',
    install_requires=[
        'matplotlib~=3.4.2', 
        'numpy~=1.21.1', 
        'fire~=0.4.0', 
        'plotly~=5.1.0',
        'SciencePlots~=1.0.8'
    ],
)
