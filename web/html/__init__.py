## @file

## @defgroup html html
## @brief HTML code elements/generation
## @ingroup web


from .html import *

from core.io import File

## @ingroup html
class htmlFile(File):
    def __init__(self, V, ext='.html'):
        super().__init__(V, ext)
