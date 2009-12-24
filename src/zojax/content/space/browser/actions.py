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

from zojax.content.type.interfaces import IContentType
from zojax.content.space.interfaces import ISpace, IContentSpace, IWorkspace
from zojax.content.actions.interfaces import IAddContentActions
from zojax.content.actions.contentactions import EditContentAction
from zojax.content.actions.contentactions import AddContent, ContentAction


class AddSpaceContentActions(ContentAction):
    interface.implements(IAddContentActions)
    component.adapts(ISpace, interface.Interface)

    def __iter__(self):
        if self.contenttype is None:
            raise StopIteration

        context = self.context
        request = self.request

        actions = []
        for ct in self.contenttype.listContainedTypes():
            action = AddContent(context, request, ct, 9999)
            actions.append((action.title, action))

        for context in self.context.values():
            if IWorkspace.providedBy(context):
                contenttype = IContentType(context, None)
                if contenttype is not None:
                    for ct in contenttype.listContainedTypes():
                        action = AddContent(context, request, ct, 9999)
                        actions.append((action.title, action))

        actions.sort()

        weight = 999
        for _t, action in actions:
            weight = weight + 1
            action.weight = weight
            yield action


class EditSpaceAction(EditContentAction):
    component.adapts(IWorkspace, interface.Interface)

    def __init__(self, context, request, view=None):
        super(EditSpaceAction, self).__init__(context.__parent__, request, view)

    def isAvailable(self):
        if not IContentSpace.providedBy(self.context):
            return False

        return super(EditSpaceAction, self).isAvailable()
