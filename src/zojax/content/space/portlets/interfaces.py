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
from zojax.content.space.interfaces import _
from zojax.portlet.interfaces import _ as pMsg
from zojax.portlet.interfaces import \
    IPortletManagerWithStatus, ENABLED, statusVocabulary
from zojax.widget.radio.field import RadioChoice

from zojax.portlets.recent.vocabulary import spaceModesVocabulary


class IContentPortletsManager(interface.Interface):
    """ content column portlets manager """


class IContentPortletsManagerConfiguration(IPortletManagerWithStatus):
    """ configuration schema """

    portletIds = schema.Tuple(
        title = _(u'Portlets'),
        value_type=schema.Choice(vocabulary = "zojax portlets"),
        default = ('portlet.recentcontent',),
        required = True)

    status = schema.Choice(
        title = pMsg(u'Status'),
        vocabulary = statusVocabulary,
        default = ENABLED,
        required = True)


class ISpacesPortlet(interface.Interface):
    """ Spaces portlet """


class IRecentContentPortlet(interface.Interface):
    """ recent contents portlet """

    rssfeed = interface.Attribute('rss feed')
    
    types = schema.List(
        title = _(u'Portal types'),
        description = _('Portal types to list in portlet.'),
        value_type = schema.Choice(
            vocabulary='zojax.portlets.recent-portaltypes'),
        default = ['__all__'],
        required = True)
    
    spaceMode = RadioChoice(
        title = _(u'Space mode'),
        default = 1,
        vocabulary=spaceModesVocabulary,
        required = True)

    number = schema.Int(
        title = _(u'Number of items'),
        description = _(u'Number of items to display'),
        default = 7,
        required = True)


class IContentRecentContentPortlet(IRecentContentPortlet):
    """ recent contents portlet for content column """

    number = schema.Int(
        title = _(u'Number of items'),
        description = _(u'Number of items to display'),
        default = 12,
        required = True)


class IWorkspacesPortlet(interface.Interface):
    """ workspaces portlet """

    descriptions = schema.Bool(
        title = _('Show dscriptions'),
        description = _('Show workspaces descriptions.'),
        default = True,
        required = False)

    workspaces = schema.List(
        title = _(u'Workspaces'),
        description = _(u'Select workspaces for this space.'),
        value_type = schema.Choice(vocabulary = 'content.space.workspaces'),
        default = [],
        required = False)
