from paver.easy import *
from paver.setuputils import setup
import urllib
import os

setup(
    name="ComicStreamer",
    packages=[],
    version="1.0",
    url="https://github.com/Tristan79/ComicStreamer",
    author="Beville/Davide Romanini/Tristan Crispijn",
    author_email="tristan@monkeycat.nl"
)

@task
@needs(["distutils.command.sdist"])
def sdist():
    """Generate docs and source distribution."""
    pass
