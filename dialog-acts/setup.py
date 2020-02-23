from setuptools import find_packages, setup

setup(
   name='dialog-acts',
   version='0.1.0a',
   description='Performs Dialogue Act Detection on text input',
   author="textability.ie",
   author_email="alexander.schutz@textability.ie",
   packages=find_packages('src'),  #same as name
   package_dir={'': 'src'},
   install_requires=[
   ]
)
