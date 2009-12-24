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
from zope.component import queryAdapter
from zope.component import queryMultiAdapter
from zope.location import LocationProxy
from zope.location.interfaces import ILocation
from zope.publisher.interfaces import NotFound, Redirect
from zope.traversing.browser import absoluteURL
from zope.security.interfaces import Unauthorized
from z3c.traverser.interfaces import ITraverserPlugin
from zojax.content.space.interfaces import IWorkspaceFactory


class PublisherPlugin(object):
    interface.implements(ITraverserPlugin)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        context = self.context

        view = queryMultiAdapter((self.context, request), name=name)
        if view is not None:
            return view

        if name in context:
            return context[name]

        factory = queryAdapter(context, IWorkspaceFactory, name)
        if factory is not None:
            if context.isEnabled(factory):
                workspace = factory.install()
                if workspace is not None:
                    if not ILocation.providedBy(workspace):
                        workspace = LocationProxy(workspace, context, name)
                    return workspace
            else:
                request.response.redirect('%s/'%absoluteURL(context, request))
                return self.context

        raise NotFound(context, name, request)
