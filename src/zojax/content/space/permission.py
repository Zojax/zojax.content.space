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
from zope import component, interface
from zope.component import queryAdapter
from zojax.content.permissions.permission import ContentPermission
from zojax.content.space.interfaces import ISpace, IWorkspaceFactory


class SpacePermission(ContentPermission):

    def isAvailable(self):
        wf = queryAdapter(self.context, IWorkspaceFactory, self.workspace)
        if wf is None or not self.context.isEnabled(wf):
            return

        return super(SpacePermission, self).isAvailable()


@component.adapter(ISpace, interface.Interface)
def spacePermissionContentTypes(space, permissions):
    if 'zojax.AddContentSpace' in permissions:
        return 'content.rootspace', 'content.space'
