
from metaL import *

def test_hello():
    hello = Object('Hello')
    assert hello.test() ==\
        '\n<object:Hello>'
    world = Object('World')
    hello // world
    assert hello.test() ==\
        '\n<object:Hello>\n\t0 : <object:World>'
