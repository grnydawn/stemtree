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
from copy import copy, deepcopy

# Node provides infrastructure, not feature
# Node attribute is dictionary or dictionary-like user object
# Node methods are replacable in part or as a whole
# Node traverse is based on user-provided search algorithm and attrs and methods
# Node infrastructure provides following services:
# - python dynamic attribute service
# - Node creation/modification/deletion

class Node(object):

    STOP_SEARCH = -1

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
            try:
                return types.MethodType(self._methods[name], self, Node)
            except TypeError:
                return types.MethodType(self._methods[name], self)
        elif name in self._shared_attrs:
            return self._shared_attrs[name]
        elif name in self._shared_methods:
            try:
                return types.MethodType(self._shared_methods[name], self, Node)
            except TypeError:
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

    def getattr_shared(self, name):

        if name in self._shared_attrs:
            return self._shared_attrs[name]
        elif name in self._shared_methods:
            try:
                return types.MethodType(self._shared_methods[name], self, Node)
            except TypeError:
                return types.MethodType(self._shared_methods[name], self)

    def setattr_shared(self, name, value):
        if callable(value):
            self._shared_methods[name] = value
        else:
            self._shared_attrs[name] = value

    def delattr_shared(self, name):
        if name in self._shared_methods:
            del self._shared_methods[name]
        elif name in self._shared_attrs:
            del self._shared_attrs[name]

    def hasattr_shared(self, name):
        return True if name in self._shared_attrs or \
            name in self._shared_methods else False

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
        return self._shared_attrs.keys() + self._shared_methods.keys() + \
            self._attrs.keys() + self._methods.keys() + dir(self)

    def treeview(self, *args):
        attrs = [a+'='+repr(getattr(self, a)) for a in args if hasattr(self, a)]
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

    def __copy__(self):

        node = self.__class__()

        # copy methods
        for name, method in self._shared_methods.items():
            node._shared_methods[name] = method
        for name, method in self._methods.items():
            node._methods[name] = method

        # copy attributes
        for name, attr in self._shared_attrs.items():
            node._shared_attrs[name] = copy(attr)
        for name, attr in self._attrs.items():
            node._attrs[name] = copy(attr)

        # copy subnodes
        for subnode in self.subnodes:
            node.add_subnode(subnode)

        return node

    def __deepcopy__(self, memo={}):
        if self in memo:
            return memo[self]
        else:
            return self.clone(memo=memo)

    def clone(self, memo={}):

        if self in memo:
            return memo[self]

        node = self.__class__()

        # save node in memo
        memo[self] = node

        # copy methods
        #for name, method in self._shared_methods.items():
        #    node._shared_methods[name] = method
        for name, method in self._methods.items():
            node._methods[name] = method

        # copy attributes
        #for name, attr in self._shared_attrs.items():
        #    node._shared_attrs[name] = deepcopy(attr, memo=memo)
        for name, attr in self._attrs.items():
            node._attrs[name] = deepcopy(attr, memo=memo)

        # clone subnodes
        for subnode in self.subnodes:
            if subnode in memo:
                node.add_subnode(memo[subnode])
            else:
                node.add_subnode(subnode.clone(memo=memo))

        return node

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

    # node manipulation
    def add_subnode(self, node, index=None):
        node.uppernode = self
        if not index:
            self.subnodes.append(node)
        else:
            self.subnodes.insert(index, node)

    def pop_subnode(self, index):
        return self.subnodes.pop(index)

    def get_subnodes(self):
        return iter(self.subnodes)

    def get_uppernodes(self):
        node = self.uppernode
        while isinstance(node, self.__class__):
            yield node
            node = node.uppernode
        return

    def get_rightnode(self, moveup=None):

        if not isinstance(self.uppernode, self.__class__):
            return None

        i = [id(n) for n in self.uppernode.subnodes].index(id(self))
        if i+1 < len(self.uppernode.subnodes):
            return self.uppernode.subnodes[i+1]
        elif moveup is True:
            return self.uppernode.get_rightnode(moveup=moveup)
        elif moveup is False:
            # check all siblings and cousins 
            pass
        else:
            pass

    def get_leftnode(self, moveup=None):

        if not isinstance(self.uppernode, self.__class__):
            return None

        i = [id(n) for n in self.uppernode.subnodes].index(id(self))
        if i > 0:
            return self.uppernode.subnodes[i-1]
        elif moveup is True:
            return self.uppernode.get_leftnode(moveup=moveup)
        elif moveup is False:
            # check all siblings and cousins 
            pass
        else:
            pass

    def insert_after(self, prevnode, node):
        previdx = self.subnodes.index(prevnode)
        self.subnodes.insert(previdx+1, node)

    def insert_before(self, nextnode, node):
        nextidx = self.subnodes.index(nextnode)
        self.subnodes.insert(nextidx, node)

    # attribute and methods manipulations
    # such as swapping methods

    def search(self, action, move, basket={}, premove=None, postmove=None):

        node = premove(self, basket) if premove is not None else self

        while isinstance(node, self.__class__):
            if action(node, basket) == self.STOP_SEARCH:
                break
            else:
                node = move(node, basket)

        return postmove(node, basket) if postmove is not None else  node
