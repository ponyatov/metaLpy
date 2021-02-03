## @file

## @defgroup js js
## @brief JavaScript
## @ingroup gen

from core.io import File

## @ingroup js
class jsFile(File):
    def __init__(self, V, ext='.js'):
        super().__init__(V, ext)
