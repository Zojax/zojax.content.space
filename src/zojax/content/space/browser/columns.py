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
import cgi
from zope import component
from zope.interface import Interface
from zope.traversing.browser import absoluteURL
from zope.app.pagetemplate import ViewPageTemplateFile

from zojax.table.column import Column
from zojax.content.space.utils import getSpace
from zojax.content.space.interfaces import _, ISpace
from zojax.content.table.interfaces import IContentsTable


class SpaceColumn(Column):
    component.adapts(Interface, Interface, IContentsTable)

    weight = 20

    name = 'space'
    title = _('Space')
    cssClass = 'ctb-space'

    template = ViewPageTemplateFile('columnspace.pt')

    def query(self, default=None):
        space = getSpace(self.content)
        if space is None:
            return

        return {'url': '%s/'%absoluteURL(space, self.request),
                'title': cgi.escape(space.title),
                'description': cgi.escape(space.description),
                'space': space}
