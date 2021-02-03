## @file

import os

from .io import IO
from .file import File
from .path import Path

## directory as container
## @ingroup io
class Dir(IO):
    def __init__(self, V):
        super().__init__(V)
        # self['path'] = Path(os.path.abspath(self.value))
        self['path'] = Path(self.value)
        try:
            os.mkdir(self.path.value)
        except FileExistsError:
            pass

    ## add file/directory using `//` operator
    def __floordiv__(self, that):
        if isinstance(that, Dir):
            that.path.value = os.path.join(self.path.value, that.path.value)
            return super().__floordiv__(that)
        if isinstance(that, File):
            that.path.value = os.path.join(self.path.value, that.path.value)
            open(that.path.value, 'a+').close()
            return super().__floordiv__(that)
        raise TypeError((type(that), that))
