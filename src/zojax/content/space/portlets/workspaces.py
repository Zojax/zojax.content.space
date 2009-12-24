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
from zope.component import getAdapters, queryMultiAdapter
from zope.security import checkPermission

from zojax.cache.view import cache
from zojax.cache.keys import ContextModified
from zojax.portlet.cache import PortletId, PortletModificationTag

from zojax.layout.interfaces import ILayout
from zojax.content.space.interfaces import \
    ISpace, IWorkspace, IWorkspaceFactory, IInactiveWorkspaceFactory


class WorkspacesPortlet(object):

    def update(self):
        context = self.context
        request = self.request

        wfactories = []
        for name, factory in getAdapters((context,), IWorkspaceFactory):
            if not IInactiveWorkspaceFactory.providedBy(factory) and \
                    not context.isEnabled(factory) or \
                    not checkPermission('zope.View', factory.get()):
                continue
            wfactories.append((
                    factory.weight, factory.title, name, factory))

        wfactories.sort()
        if self.workspaces:
            wfactories = [(n, f) for _w, _t, n, f in wfactories \
                              if n in self.workspaces]
        else:
            wfactories = [(n, f) for _w, _t, n, f in wfactories]

        workspaces = []
        for name, factory in wfactories:
            workspaces.append(
                 {'name': name,
                  'title': factory.title,
                  'description': factory.description,
                  'icon': queryMultiAdapter((factory,request), name='zmi_icon'),
                  })

        self.wfs = workspaces

    @cache(PortletId(), PortletModificationTag, ContextModified)
    def updateAndRender(self):
        return super(WorkspacesPortlet, self).updateAndRender()
