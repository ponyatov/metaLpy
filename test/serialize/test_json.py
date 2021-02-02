from metaL import *

def test_hello():
    hello = Object('Hello') // Object('World')
    assert hello.json() ==\
        '{"tag":"object","val":"Hello"}'
