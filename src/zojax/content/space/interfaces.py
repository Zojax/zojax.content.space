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
from zope import schema, interface
from zope.i18nmessageid import MessageFactory
from zojax.content.type.interfaces import IContent
from zojax.widget.checkbox.field import CheckboxList
from zojax.content.feeds.interfaces import IRSS2Feed

_ = MessageFactory('zojax.content.space')


class ISpace(IContent):
    """ base interface for space """

    id = interface.Attribute('Unique space ID')

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'Space title.'),
        default = u'',
        missing_value = u'',
        required = True)

    description = schema.Text(
        title = _(u'Description'),
        description = _(u'Small description of space.'),
        default = u'',
        missing_value = u'',
        required = False)

    def isEnabled(workspaceFactory):
        """Is workspace factory enabled."""


class IRootSpace(interface.Interface):
    """ marker interface for root space """


class IContentSpace(ISpace):
    """ content space """


class IWorkspacesManagement(interface.Interface):
    """ workspace management """

    workspaces = CheckboxList(
        title = _(u'Workspaces'),
        description = _(u'Select workspaces for this space.'),
        vocabulary = 'content.space.workspaces',
        default = [],
        required = False)

    enabledWorkspaces = schema.List(
        title = _('Workspaces sorting and visibility'),
        description = _('Configure what workspaces have to be shown and in what order'),
        value_type = schema.Choice(
            vocabulary='content.space.enabledworkspaces'),
        default = [],
        required = False)

    defaultWorkspace = schema.Choice(
        title = _(u'Default workspace'),
        description = _(u'Select default workspace for this space.'),
        vocabulary = 'content.space.enabledworkspaces',
        required = False,
        default = 'overview')


class IRootSpaceType(interface.Interface):
    """ root space type """


class IContentSpaceType(interface.Interface):
    """ content space type """


class ISpaceContentType(interface.Interface):
    """ space content type """


class IContentSpaceLayout(interface.Interface):
    """ content space layout settings """

    showTabs = schema.Bool(
        title = _(u'Show space tabs'),
        description = _('Space Tabs represent space workspaces, such as Documents, Photos, Blog, etc.'),
        required = False,
        default = True)

    showHeader = schema.Bool(
        title = _(u'Show space header'),
        required = False,
        default = True)


# workspace

class IWorkspace(interface.Interface):
    """ Workspace inside space """

    space = interface.Attribute('Space')


class IWorkspaceFactory(interface.Interface):
    """ workspace factory """

    name = interface.Attribute('name')

    title = schema.TextLine(
        title = u'Title',
        description = u'Workspace title.',
        required = True)

    description = schema.TextLine(
        title = u'Description',
        description = u'Short description of workspace.',
        required = False)

    weight = schema.Int(
        title = u'Weight',
        description = u'Workspace weight for sorting.',
        required = True)

    def get():
        """ return installed workspace """

    def install():
        """ Create workspace """

    def uninstall():
        """ Remove workspace """

    def isInstalled():
        """ Is workspace installed """

    def isAvailable():
        """ Is this workspace available """


class IInactiveWorkspaceFactory(interface.Interface):
    """ marker interface for inactive workspace factories """


# overview workspace

class IOverviewWorkspace(IWorkspace):
    """ space overview workspace """


class IOverviewWorkspaceFactory(IWorkspaceFactory):
    """ overview workspace factory """


# space permission

class ISpacePermission(interface.Interface):
    """ space permission """

    workspace = schema.TextLine(
        title = u'Workspace factory name',
        required = True)


# contents rss feed

class IContentsRSSFeed(IRSS2Feed):
    pass
