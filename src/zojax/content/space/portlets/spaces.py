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
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.traversing.api import getPath
from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite

from zojax.catalog.interfaces import ICatalog
from zojax.content.space.interfaces import ISpace


class SpacesPortlet(object):

    def update(self):
        context = getSite()
        self.context = context

        results = getUtility(ICatalog).searchResults(
            searchContext=context,
            type={'any_of': ('content.space',)},
            isDraft={'any_of': (False,)})

        count = 1000
        spaces = []
        for space in results:
            url = '%s/'%absoluteURL(space, self.request)

            c = url.count('/')
            if c < count:
                count = c

            spaces.append((c, space.title,
                           {'title': space.title,
                            'description': space.description,
                            'url': url,
                            'level': c,
                            'space': space}))

        spaces.sort()
        spaces = [info for c, t, info in spaces]
        for info in spaces:
            info['level'] = info['level'] - count

        self.spaces = spaces

        super(SpacesPortlet, self).update()

    def isAvailable(self):
        return bool(self.spaces)
