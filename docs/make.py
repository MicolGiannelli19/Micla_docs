#!/usr/bin/env python3
from pathlib import Path
import shutil

from pdoc import pdoc
from pdoc import render

here = Path(__file__).parent
out = here / "docs" / "Python"

# Render parts of pdoc's documentation into docs/api...
render.configure(template_directory=here / "pdoc-template")
pdoc("!!!!FILES TO RUN OUTPUT ON!!!!!.py", output_directory=out)

# ...and rename the .html files to .md so that mkdocs picks them up!
for f in out.glob("**/*.html"):
    f.rename(f.with_suffix(".md"))