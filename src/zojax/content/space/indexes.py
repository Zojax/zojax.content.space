##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds
from zc.catalog.catalogindex import ValueIndex, SetIndex
from zojax.catalog.utils import Indexable
from zojax.content.space.interfaces import ISpace


def contentSpace():
    return ValueIndex(
        'value', Indexable('zojax.content.space.indexes.ContentSpace'))


def contentSpaces():
    return SetIndex(
        'value', Indexable('zojax.content.space.indexes.ContentSpaces'))


class ContentSpace(object):

    def __init__(self, content, default=None):
        self.value = default

        while not ISpace.providedBy(content):
            content = getattr(content, '__parent__', None)
            if content is None:
                break

        if content is not None:
            self.value = getUtility(IIntIds).queryId(removeAllProxies(content))


class ContentSpaces(object):

    def __init__(self, content, default=None):
        spaces = []
        while content is not None:
            if ISpace.providedBy(content):
                spaces.append(content)

            content = getattr(content, '__parent__', None)

        ids = getUtility(IIntIds)

        value = []
        for space in spaces:
            id = ids.queryId(removeAllProxies(space))
            if id is not None:
                value.append(id)

        self.value = value
