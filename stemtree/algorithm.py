# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

"""Tree Algorithms for Stemtree.
"""

def assemble_subtrees(*nodeset):
    trees = []

    # append node in a tree
    def append(trees, node):

        # setup 
        if not hasattr(node, '_subnodes'):
            node._subnodes = [None for _ in range(len(node.subnodes))]
        if not hasattr(node, '_uppernode'):
            node._uppernode = None

        # add a root of one of trees if node is uppernode
        for idx, tnode in enumerate(trees):
            if tnode.uppernode is node:
                tnode._uppernode = node
                node._subnodes[node.subnodes.index(tnode)] = tnode
                trees[idx] = node
                return

        # collect uppernodes of node
        uppernodes = []
        uppernode = node
        while uppernode is not None:
            uppernodes.append(uppernode)
            uppernode = uppernode.uppernode

        # attach node into a tree
        for tnode in trees:
            try:
                idx = uppernodes.index(tnode)
                connected = True
                for unode in reversed(uppernodes[1:idx]):
                    if unode in tnode._subnodes:
                        tnode = unode
                    else:
                        connected = False
                        break
                if connected:
                    tnode._subnodes[tnode.subnodes.index(node)] = node
                    node._uppernode = tnode
                    return
            except ValueError:
                pass

        # new root node
        trees.append(node)


    def switch(tree):
        tree.uppernode = tree._uppernode
        tree.subnodes = []
        for snode in tree._subnodes:
            if snode is not None:
                tree.subnodes.append(switch(snode))
        return tree

    # main routine
    for nodes in nodeset:
        try:
            for node in nodes:
                append(trees, node)
        except TypeError:
            append(trees, node)

    # reduce trees
    _trees = []
    for tree in trees:
        append(_trees, tree)

    # replace subnodes and uppernode
    for tree in _trees:
        switch(tree)

    return _trees
