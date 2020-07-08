from setuptools import find_packages, setup

setup(
   name='entity-detect-and-resolve',
   version='0.1.0a',
   description='Performs Entity Detection and Resolution on text input',
   author="textability.ie",
   author_email="alexander.schutz@textability.ie",
   packages=find_packages('src'),
   package_dir={'': 'src'},
   install_requires=[
      'spacy',
      'maya'
   ]
)