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
from zojax.content.type.interfaces import IItem
from zojax.content.type.item import PersistentItem
from zojax.content.type.container import ContentContainer
from zojax.content.space.interfaces import IContentSpace
from zojax.content.space.interfaces import IWorkspace, IWorkspaceFactory
from zojax.content.space.workspace import WorkspaceFactory


class ITestWorkspace(IItem, IWorkspace):
    pass


class ITestWorkspaceFactory(IWorkspaceFactory):
    pass


class TestWorkspace(ContentContainer):
    interface.implements(ITestWorkspace)

    __name__ = 'test'

    def __init__(self, title=u''):
        super(TestWorkspace, self).__init__()

        self.title = title


class TestWorkspaceFactory(WorkspaceFactory):
    component.adapts(IContentSpace)
    interface.implements(ITestWorkspaceFactory)

    name = 'test'
    title = u'Test workspace'
    description = u''
    weight = 10

    factory = TestWorkspace


class TestWorkspaceFactory2(TestWorkspaceFactory):

    def isAvailable(self):
        return False


class ITestContent(IItem):
    pass

class TestContent(PersistentItem):
    interface.implements(ITestContent)



class ITestContent2(IItem):
    pass

class TestContent2(PersistentItem):
    interface.implements(ITestContent2)
