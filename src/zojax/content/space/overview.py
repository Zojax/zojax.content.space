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
from zope import interface, component
from zope.location import Location

from interfaces import _, IContentSpace
from interfaces import IOverviewWorkspace, IOverviewWorkspaceFactory


class OverviewWorkspace(Location):
    interface.implements(IOverviewWorkspace)

    __name__ = 'overview'
    title = _(u'Overview')


class OverviewWorkspaceFactory(object):
    component.adapts(IContentSpace)
    interface.implements(IOverviewWorkspaceFactory)

    name = 'overview'
    title = _(u'Overview')
    description = _(u'Space customizable overview.')
    weight = 0

    def __init__(self, space):
        self.space = space

    def get(self):
        view = OverviewWorkspace()
        view.__parent__ = self.space
        return view

    install = get

    def uninstall(self):
        pass

    def isInstalled(self):
        return False

    def isAvailable(self):
        return True
