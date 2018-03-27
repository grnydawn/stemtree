# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from collections import OrderedDict
from .node import Node

def text(obj):
    return ''.join([n.line for n in obj])

class SourceLines(Node):

    #@property
    #def text(self):
    #    return ''.join([n.line for n in self])

    def __init__(self, path):

        super(self.__class__, self).__init__(attr_factory=OrderedDict)
        self.name = path
        self.text = text

        with open(path) as f:
            for i, line in enumerate(f):
                node = Node(attr_factory=OrderedDict)
                node.line = line
                node.lineno = i
                node.name = str(i+1)
                self.add_subnode(node)

