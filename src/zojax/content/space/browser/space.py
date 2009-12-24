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
from zope.security import checkPermission
from zope.component import getAdapters, queryAdapter, getMultiAdapter
from zojax.content.space.interfaces import \
    IWorkspaceFactory, IOverviewWorkspaceFactory


class ContentSpace(object):

    def __call__(self, *args, **kw):
        workspaces = []
        space = self.context
        default = space.defaultWorkspace

        factory = queryAdapter(space, IWorkspaceFactory, default)
        if factory is not None:
            if space.isEnabled(factory):
                if IOverviewWorkspaceFactory.providedBy(factory):
                    return getMultiAdapter(
                        (space, self.request), name='overview')()

                self.request.response.redirect('./%s/'%default)
                return

        for name, factory in getAdapters((space,), IWorkspaceFactory):
            if space.isEnabled(factory) and \
                    checkPermission('zope.View', factory.get()):
                workspaces.append((factory.weight, factory.title, name))

        if workspaces:
            workspaces.sort()
            self.request.response.redirect('./%s/'%workspaces[0][2])
        else:
            self.request.response.redirect('./listing.html')
