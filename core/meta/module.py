## @file

from .meta import Meta
from core.io import File

import os, re

## @ingroup meta
class Module(Meta):
    def __init__(self, V):
        az = r'[a-z]+'
        if isinstance(V, File):
            fn = os.path.split(V.value)[-1]
            V = re.findall(az, fn)[0]
        assert isinstance(V, str)
        assert re.match(f'^{az}$', V)
        super().__init__(V)
