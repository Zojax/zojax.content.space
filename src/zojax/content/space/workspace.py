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
from zope import event, interface, component
from zope.lifecycleevent import ObjectCreatedEvent
from zope.security.proxy import removeSecurityProxy
from zope.copypastemove.interfaces import IObjectCopier, IObjectMover

from interfaces import IWorkspace, IWorkspaceFactory


class WorkspaceFactory(object):

    name = u''
    weight = 999999
    title = u''
    description = ''

    factory = None

    def __init__(self, space):
        self.space = space

    def get(self):
        return self.space.get(self.name)

    def install(self):
        ws = self.space.get(self.name)

        if ws is None:
            ws = self.factory(title = self.title)
            event.notify(ObjectCreatedEvent(ws))
            removeSecurityProxy(self.space)[self.name] = ws

            ws = self.space.get(self.name)

        return ws

    def uninstall(self):
        del self.space[self.name]

    def isInstalled(self):
        return self.name in self.space

    def isAvailable(self):
        return True


class WorkspaceCopier(object):
    component.adapts(IWorkspace)
    interface.implements(IObjectCopier)

    def __init__(self, object):
        self.context = object

    def copyTo(self, target, new_name=None):
        raise RuntimeError('Object is not copyable')

    def copyable(self):
        return False

    def copyableTo(self, target, name=None):
        return False


class WorkspaceMover(object):
    component.adapts(IWorkspace)
    interface.implements(IObjectMover)

    def __init__(self, object):
        self.context = object

    def moveTo(self, target, new_name=None):
        raise RuntimeError('Object is not moveable')

    def moveable(self):
        return False

    def moveableTo(self, target, name=None):
        return False
