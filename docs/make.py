#!/usr/bin/env python3
from pathlib import Path

# import shutil

from pdoc import pdoc, render

# Something which copies the contents of ../client/python/twinlab/client.py and creates a file in this folder called "Python_Client_API.py"
source_directory = Path("../example1")
output_directory = Path(__file__).parent / "docs" / "Python"

# Render parts of pdoc's documentation into docs/api...
render.configure(template_directory=Path(__file__).parent / "pdoc-template")

# Use pdoc to generate documentation for all modules in the source directory
pdoc(source_directory, output_directory=output_directory)


# ...and rename the .html files to .md so that mkdocs picks them up!
for f in output_directory.glob("**/*.html"):
    f.rename(f.with_suffix(".md"))


# TODO: change it so that it doesn't create the markdown file with the name of the directory
# TODO: understand why the same doesn't work with the twinlab module and see if these are issues related to the .env file
