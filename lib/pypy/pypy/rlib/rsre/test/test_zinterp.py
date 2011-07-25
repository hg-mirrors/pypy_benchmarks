# minimal test: just checks that (parts of) rsre can be translated

from pypy.rpython.test.test_llinterp import gengraph
from pypy.rlib.rsre import rsre_core

def main(n):
    assert n >= 0
    pattern = [n] * n
    string = chr(n) * n
    rsre_core.search(pattern, string)
    #
    unicodestr = unichr(n) * n
    ctx = rsre_core.UnicodeMatchContext(pattern, unicodestr,
                                        0, len(unicodestr), 0)
    rsre_core.search_context(ctx)
    #
    return 0


def test_gengraph():
    t, typer, graph = gengraph(main, [int])
