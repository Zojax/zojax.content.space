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
from zope.app.intid.interfaces import IIntIds
from zojax.content.type.container import ContentContainer
from zojax.content.space.interfaces import IContentSpace, IWorkspacesManagement


class ContentSpace(ContentContainer):
    interface.implements(IContentSpace, IWorkspacesManagement)

    showTabs = True
    showHeader = True
    workspaces = ('overview',)
    enabledWorkspaces = ()
    defaultWorkspace = 'overview'

    @property
    def id(self):
        return component.getUtility(IIntIds).getId(self)

    def isEnabled(self, workspaceFactory):
        return workspaceFactory.isAvailable() and \
            workspaceFactory.name in self.workspaces
