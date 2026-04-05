
# Command line interface for laro.
# For now, the only use of this for generating template files.

# Libraries
import click
from shutil import copyfile
import os, sys

# Code
@click.group()
def cli() -> None:
    # We'd preferrably have a welcome message here.
    pass

# Define commands here:
@click.command()
def template() -> None:
    # copyfile('template.py', os.getcwd())
    pass

# Add commands here:
cli.add_command(template)

# Run
if __name__ == "__main__":
    cli() # For debug only

