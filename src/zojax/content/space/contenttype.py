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
from zope.component import \
    getUtility, getAdapter, queryAdapter, queryMultiAdapter
from zojax.content.space.interfaces import IWorkspaceFactory
from zojax.content.draft.contenttype import DraftedContentType
from zojax.content.draft.interfaces import IDraftContainer, IDraftContentType


class SpaceContentType(DraftedContentType):

    workspaceFactory = ''

    @property
    def container(self):
        return getAdapter(
            self.context, IWorkspaceFactory, self.workspaceFactory).install()

    def checkObject(self, container, name, content):
        return True

    def isAvailable(self):
        if super(SpaceContentType, self).isAvailable():
            wf = queryAdapter(
                self.context, IWorkspaceFactory, self.workspaceFactory)
            if wf is None or not self.context.isEnabled(wf):
                return False
            return True
        else:
            return False
