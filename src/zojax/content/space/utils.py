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
from zojax.catalog.interfaces import ICatalog
"""

$Id$
"""
from zope.component import getAdapters
from zope.traversing.api import getParents
from zope.security.proxy import removeSecurityProxy
from zojax.content.type.interfaces import IDraftedContent
from zojax.content.space.interfaces import \
    IWorkspaceFactory, IWorkspace, ISpace


def createWorkspaces(space, event=None):
    if IDraftedContent.providedBy(space):
        return

    for name, factory in getAdapters((space,), IWorkspaceFactory):
        if space.isEnabled(factory):
            if not factory.isInstalled():
                factory.install()
        elif factory.isInstalled():
            ws = removeSecurityProxy(factory.install())
            if not getattr(ws, '__remove__', False):
                ws.__remove__ = True
                factory.uninstall()


def getSpace(ob, default=None):
    while not ISpace.providedBy(ob):
        ob = ob.__parent__
        if ob is None:
            return default
    return ob


def getSpacePath(ob, reversed=False):
    path = [ob] + getParents(ob)
    if reversed:
        path.reverse()
    return filter(ISpace.providedBy, path)


def getWorkspace(ob):
    while not IWorkspace.providedBy(ob):
        ob = ob.__parent__
        if ob is None:
            return
    return ob

def getSubspaces(space):
    return getUtility(ICatalog).searchResults(
            searchContext=space,
            type={'any_of': ('content.space',)},
            isDraft={'any_of': (False,)})
