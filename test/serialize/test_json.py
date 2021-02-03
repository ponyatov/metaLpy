from metaL import *

## @name ISerialize

## serialize `hello/world` to .json
## @ingroup test
def test_hello():
    hello = Object('Hello') // Object('World')
    assert hello.json() ==\
        '{"tag":"object","val":"Hello","nest":[{"tag":"object","val":"World"}]}'
