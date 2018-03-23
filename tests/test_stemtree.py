#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `stemtree` package."""

import pytest
import copy


from stemtree import Node

@pytest.fixture(scope="module")
def test_add():

    node = Node()

    a = Node()
    b = Node()
    node.add_subnode(a)
    node.add_subnode(b)

    assert a in node
    assert b in node

    return node

@pytest.fixture(scope="module")
def test_attr(test_add):
    def dummy(obj):
        return "Hello"

    def sum2(obj, x, y):
       return x + y

    assert isinstance(test_add, Node)
    test_add.somevalue = 1
    assert test_add.somevalue == 1
    test_add.dummy = dummy
    assert test_add.dummy() == "Hello"
    with pytest.raises(AttributeError):
        test_add._attrs = dummy
    test_add.sum = sum2
    assert test_add.sum(1,2) == 3
    delattr(test_add, "dummy")
    assert not hasattr(test_add, "dummy")

    return test_add

def test_copy(test_attr):
    newnode = copy.copy(test_attr)
    assert test_attr == newnode
    assert newnode == test_attr
    for k, v in test_attr._attrs.items():
        assert newnode._attrs[k] == v
        assert v == newnode._attrs[k]
    for k, v in newnode._attrs.items():
        assert test_attr._attrs[k] == v
        assert v == newnode._attrs[k]

    deepnode = copy.deepcopy(test_attr)
    assert test_attr == deepnode
    assert deepnode == test_attr
    for k, v in test_attr._attrs.items():
        assert deepnode._attrs[k] == v
        assert v == deepnode._attrs[k]
    for k, v in deepnode._attrs.items():
        assert test_attr._attrs[k] == v
        assert v == deepnode._attrs[k]

    for index in range(len(test_attr)):
        test_attr[index].data = 1
        assert not hasattr(deepnode[index], "data")

    for index in range(len(test_attr)):
        assert hasattr(newnode[index], "data")

    return test_attr

def test_subnodes(test_attr):
    assert len(test_attr) == 2
    n = test_attr.pop_subnode(0)
    assert len(test_attr) == 1
    test_attr.add_subnode(n)
    assert n == test_attr[1]

