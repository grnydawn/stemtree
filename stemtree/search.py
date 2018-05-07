# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

"""Search Algorithms for Stemtree.
"""

def DFS_LF(node, basket):
    """Depth-first search from the left of a tree."""

    if len(node.subnodes) > 0:
        return node.subnodes[0]
    else:
        return node.get_rightnode(moveup=True)

def DFS_RF(node, basket):
    """Depth-first search from the right of a tree."""
    if len(node.subnodes) > 0:
        return node.subnodes[-1]
    else:
        return node.get_leftnode(moveup=True)

def UPWARDS(node, basket):
    """Upward search."""
    return node.uppernode

#def BFS_LF(node, basket):
#    """Breadth-first search from the left of a tree."""
#
#    node = node.get_rightnode(moveup=False)
#    if isinstance(node, node.__class__):
#        return node
#
#    if len(node.subnodes) > 0:
#        return node.subnodes[0]
#    else:
#        return None
#
#def BFS_RF(node, basket):
#    """Breadth-first search from the right of a tree."""
#
#    node = node.get_leftnode(moveup=False)
#    if isinstance(node, node.__class__):
#        return node
#
#    if len(node.subnodes) > 0:
#        return node.subnodes[-1]
#    else:
#        return None
#
#def DFS_UP(node, basket):
#    """Breadth-first search from the left of a tree."""
#
#    if len(node.subnodes) > 0:
#        while len(node.subnodes) > 0:
#            node = node.subnodes[0]
#        return node
#    else:
#        node = node.get_rightnode(moveup=True)
#        if isinstance(node, node.__class__):
#            return node
#
#        if len(node.subnodes) > 0:
#            return node.subnodes[0]
#        else:
#            return None
#
