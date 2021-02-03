## @file

from .io import *
from .path import Path

## file as container
## @ingroup io
class File(IO):
    ## @param[in] V file name (w/o `.ext`)
    ## @param[in] ext optional file `V.extension`:
    ## inherited extFile defines custom `.ext`
    ## @param[in] comment line comment start marker
    ## @param[in] commend line comment end marker
    def __init__(self, V, ext='', comment='', commend=''):
        if isinstance(V, Object):
            V = V.value
        assert isinstance(V, str)
        assert isinstance(ext, str)
        super().__init__(V + ext)
        self.comment = comment
        self.commend = commend
        self['path'] = Path(self.value)
