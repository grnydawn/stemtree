# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

"""Search Algorithms for Stemtree.
"""

def DFS_LF(obj, basket):
    """Depth-first search from the left of a tree."""

    if len(obj.subnodes) > 0:
        return obj.subnodes[0]
    else:
        return obj.get_rightnode(moveup=True)

def DFS_RF(obj, basket):
    """Depth-first search from the right of a tree."""
    if len(obj.subnodes) > 0:
        return obj.subnodes[-1]
    else:
        return obj.get_leftnode(moveup=True)

def BFS_LF(obj, basket):
    """Breadth-first search from the left of a tree."""

    node = obj.get_rightnode(moveup=False)
    if isinstance(node, obj.__class__):
        return node

    if len(obj.subnodes) > 0:
        return obj.subnodes[0]
    else:
        return None

def BFS_RF(obj, basket):
    """Breadth-first search from the right of a tree."""

    node = obj.get_leftnode(moveup=False)
    if isinstance(node, obj.__class__):
        return node

    if len(obj.subnodes) > 0:
        return obj.subnodes[-1]
    else:
        return None

