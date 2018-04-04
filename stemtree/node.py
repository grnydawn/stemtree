# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

"""Flexible Tree Library.
- flexible tree structure manipulation
- flexible node attribute management
- flexible node method instantiation
"""

import types
from copy import deepcopy
import abc

# Node provides tree structure and flexible attribute and methods infrastructure
# attribute can be MutableMapping that can have its own context
# methods can be entirely replaced so that node can have very different capability

# Node provides infrastructure, not feature
# Node attribute is dictionary or dictionary-like user object
# Node methods are replacable in part or as a whole
# Node traverse is based on user-provided search algorithm and attrs and methods
# Node infrastructure provides following services:
# - python dynamic attribute service
# - Node creation/modification/deletion


# Reader Writer, ... are classes that
# - produces Nodes that are equiped with some default attributes and feature methods
# - Reader: One of the feature methods read data and transfom it into Nodes
# - Writer: Transfor Nodes into external data format
# - Transformer: transform Nodes into another Nodes with possible changes on _attrs,
#   _methods, and structure itself


class Node(object):

    __slots__ = ['_attrs', '_methods', 'uppernode', 'subnodes']

    _shared_attrs = {}
    _shared_methods = {}

    def __init__(self, uppernode=None, subnodes=None, attrs=None, methods=None,
        shared_attrs=None, shared_methods=None):

        object.__setattr__(self, '_attrs', attrs if attrs else {})
        object.__setattr__(self, '_methods', methods if methods else {})

        if shared_attrs:
            self._shared_attrs.update(shared_attrs)
        if shared_methods:
            self._shared_methods.update(shared_methods)

        self.uppernode = uppernode
        self.subnodes = subnodes if subnodes else []

    # attributes
    def __getattr__(self, name):

        if name in self._attrs:
            return self._attrs[name]
        elif name in self._methods:
            return types.MethodType(self._methods[name], self)
        elif name in self._shared_attrs:
            return self._shared_attrs[name]
        elif name in self._shared_methods:
            return types.MethodType(self._shared_methods[name], self)

        raise AttributeError("'%s' object has no attribute '%s'."% (
            self.__class__.__name__, name))

    def __setattr__(self, name, value):

        if name in ('_attrs', '_methods', '_shared_attrs', '_shared_methods'):
            if name in dir(self):
                raise AttributeError("'%s' attribute is not mutable."%name)
            else:
                object.__setattr__(self, name, value)
        elif name in self.__slots__:
            object.__setattr__(self, name, value)
        elif name in dir(self):
            raise AttributeError("'%s' attribute is not mutable."%name)
        elif callable(value):
            self._methods[name] = value
        else:
            self._attrs[name] = value

    def __delattr__(self, name):

        if name in ('_attrs', '_methods', '_shared_attrs', '_shared_methods'):
            raise AttributeError("'%s' attribute is not mutable."%name)
        elif name in self._methods:
            del self._methods[name]
        elif name in self._attrs:
            del self._attrs[name]
        else:
            object.__delattr__(self, name)

    def __hasattr__(self, name):

        try:
            getattr(self, name)
            return True
        except:
            return False

    # equality
    def __eq__(self, other):
        """Equals when having the same public attributes/values"""
        try:
            for k, v in self._attrs.items():
                if other._attrs[k] != v:
                    return False
            return True
        except Exception as e:
            return False

    def __ne__(self, other):
        """Not equals when having any different public attributes/values"""
        try:
            for k, v in self._attrs.items():
                if other._attrs[k] == v:
                    return False
            return True
        except:
            return True

    # representation
    def __hash__(self):
        return id(self)

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        else:
            return self.__class__.__name__

    def __unicode__(self):
        if hasattr(self, 'name'):
            return u'%s'%self.name
        else:
            return u'%s'%self.__class__.__name__

    def __repr__(self):
        return "%s %s"%(self.__class__, str(self))

    def dirall(self):
        return ( self._attrs.keys(), self._methods.keys(), dir(self) )

    def treeview(self, *args):
        attrs = [a+'='+str(getattr(self, a)) for a in args if hasattr(self, a)]
        lines = [str(self)+(' (%s)'%', '.join(attrs) if attrs else '')]
        lines.extend(["-"+n.treeview(*args) for n in self.subnodes])
        return "\n".join(lines).replace("\n-", "\n---|")

    # sequences
    def __len__(self):
        return len(self.subnodes)

    def __iter__(self):
        return iter(self.subnodes)

    def __reversed__(self):
        return reversed(self.subnodes)

    def __getitem__(self, key):
        return self.subnodes[key]

    def __setitem__(self, key, value):
        self.subnodes[key] = value

    def __delitem__(self, key):
        del self.subnodes[key]

    def __contains__(self, item):
        return item in self.subnodes

    #def __missing__(self, key):
    #    return item in self.subnodes

    # copying
    def local_deepcopy(self):
        newnode = self.__class__(uppernode=self.uppernode, subnodes=[],
            attrs=deepcopy(self._attrs), methods=deepcopy(self._methods))
#        for name, value in self._attrs.items():
#            setattr(newnode, name, deepcopy(value))
#        for name, value in self._methods.items():
#            setattr(newnode, name, deepcopy(value))
        return newnode

    def __copy__(self):
        newnode = self.local_deepcopy()
        for subnode in self.subnodes:
            newnode.add_subnode(subnode)
        return newnode

    def __deepcopy__(self, memo={}):
        newnode = self.local_deepcopy()
        for subnode in self.subnodes:
            newnode.add_subnode(deepcopy(subnode, memo=memo))
        return newnode

    # pickling
    def __getinitargs__(self):
        import pdb; pdb.set_trace()

    def __getnewargs__(self):
        import pdb; pdb.set_trace()

    def __getstate__(self):
        import pdb; pdb.set_trace()

    def __setstate__(self, state):
        import pdb; pdb.set_trace()

    def __reduce__(self):
        import pdb; pdb.set_trace()

    def __reduce_ex__(self):
        import pdb; pdb.set_trace()

    # subnodes functions
    def add_subnode(self, node, index=None):
        node.uppernode = self
        if not index:
            self.subnodes.append(node)
        else:
            self.subnodes.insert(index, node)

    def pop_subnode(self, index):
        return self.subnodes.pop(index)

    def get_subnodes(self):
        return self.subnodes

    # attribute and methods manipulations
    # such as swapping methods

    # traversing
    def traverse(self, search_algorithm, event_handlers, data_collector):
        pass
