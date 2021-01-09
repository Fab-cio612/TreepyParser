from . import dom_tree

#How the Parser works:
#
#
#
#
#
#
#
#
#
#
#
#
#

def parse(html):
    #list for self closing tags
    self_closing = ["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"]
    #stack for nodes
    stack = []
    #states:
    #
    #
    #
    #
    #
    state = 0
    #pointers
    pointer = 0
    lagging_pointer = 0

    #parser loop
    for c in html:
        pass
    return