
# Code from setuputils docs
# Apparently, the src layout requires the module to be installed (in development mode) for testing
# purposes* which can be impractical in some situations.
import os
import sys

if not __package__:
    # Make CLI runnable from source tree with
    #    python src/package <- this is the command to be used on the cmd. No modifications are needed.
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)

from . import cli
cli.cli()   # CLI access.