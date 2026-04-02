
# Setup for compiling the pyx files.

# Libraries
from Cython.Build import cythonize
from setuptools import setup, Extension
from os.path import join

# To compile the files, enter the following in the command line:
# Move to the proper directory first using "cd" then;
# python setup.py build_ext --inplace

# Code
ext_modules = [
    # Format for adding cython modules:
    # Extension(
    #     name = "laro.[module name without file extension]",
    #     sources = [   # Add cython modules here
    #         join("src", "laro", "[module name with file extension]")
    #     ]
    # ),
]

setup(
    ext_modules=cythonize(
        ext_modules, 
        #   When True, creates an html file displaying the amount of python interaction per line of code.
        #   Just see the Cython docs man
        nthreads=3,
        annotate = False
    )
)