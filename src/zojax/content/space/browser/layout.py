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
from zope import interface, schema
from zope.security import checkPermission
from zope.component import \
    getAdapters, getMultiAdapter, queryMultiAdapter, queryAdapter
from zope.traversing.browser import absoluteURL
from z3c.breadcrumb.interfaces import IBreadcrumb
from zojax.layoutform import Fields, PageletEditForm
from zojax.content.forms.interfaces import IContentWizard

from zojax.content.space.interfaces import \
    _, ISpace, IContentSpaceLayout, IOverviewWorkspace, \
    IWorkspace, IWorkspaceFactory, IWorkspacesManagement, \
    IInactiveWorkspaceFactory


class LayoutSettings(PageletEditForm):

    title = label = _(u'Space layout')
    fields = Fields(IContentSpaceLayout)
    prefix = 'content.space.'


class SpaceLayout(object):

    workspaces = ()
    showHeader = True

    def update(self):
        super(SpaceLayout, self).update()

        wsname = u''
        ws = self.mainview
        while not ISpace.providedBy(ws):
            if IWorkspace.providedBy(ws):
                wsname = ws.__name__
                break
            ws = ws.__parent__

        if not wsname:
            wsname = self.mainview.__name__

        self.workspace = ws

        context = self.context
        request = self.request

        if IContentSpaceLayout.providedBy(context):
            self.showHeader = context.showHeader
            self.title = context.title
        else:
            self.title = getMultiAdapter((context, request), IBreadcrumb).name

        if IContentSpaceLayout.providedBy(context) and not context.showTabs:
            return

        wfactories = []

        management = IWorkspacesManagement(context, None)
        if IWorkspacesManagement.providedBy(management):
            if management.enabledWorkspaces:
                for name in management.enabledWorkspaces:
                    factory = queryAdapter(context, IWorkspaceFactory, name)
                    if factory is not None and \
                            checkPermission('zope.View', factory.get()):
                        wfactories.append((name, factory))

        if not wfactories:
            for name, factory in getAdapters((context,), IWorkspaceFactory):
                if not IInactiveWorkspaceFactory.providedBy(factory) and \
                        not context.isEnabled(factory) or \
                        not checkPermission('zope.View', factory.get()):
                    continue
                wfactories.append((
                        factory.weight, factory.title, name, factory))

            wfactories.sort()
            wfactories = [(n, f) for _w, _t, n, f in wfactories]

        workspaces = []
        for name, factory in wfactories:
            workspaces.append(
                 {'name': name,
                  'title': factory.title,
                  'description': factory.description,
                  'selected': name == wsname,
                  'icon': queryMultiAdapter((factory,request), name='zmi_icon'),
                  })

        self.workspaces = workspaces

    def editable(self):
        if checkPermission('zojax.ModifyContent', self.context):
            return absoluteURL(self.context, self.request)


class WorkspaceLayout(object):

    workspaces = ()

    def update(self):
        super(WorkspaceLayout, self).update()

        wsname = u''
        ws = self.mainview
        while not ISpace.providedBy(ws):
            if IWorkspace.providedBy(ws) and \
                    not IOverviewWorkspace.providedBy(ws):
                break
            ws = ws.__parent__

        self.workspace = ws

        view = self.mainview
        while not IContentWizard.providedBy(view):
            view = view.__parent__
            if view is None:
                break

        self.wizard = view is not None
