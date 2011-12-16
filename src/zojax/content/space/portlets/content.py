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
from zope import component, interface
from zope.component import getUtility, getUtilitiesFor, queryMultiAdapter
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL
from zope.dublincore.interfaces import IDCTimes
from zope.lifecycleevent import IObjectModifiedEvent
from zope.app.intid.interfaces import IIntIds

from zojax.catalog.interfaces import ICatalog
from zojax.formatter.utils import getFormatter
from zojax.content.type.interfaces import IContentViewView, IItem
from zojax.ownership.interfaces import IOwnership
from zojax.principal.profile.interfaces import IPersonalProfile

from zojax.cache.view import cache
from zojax.cache.keys import Principal
from zojax.cache.timekey import TagTimeKey, each20minutes
from zojax.portlet.cache import PortletId, PortletModificationTag

from zojax.content.space.utils import getSpace
from zojax.content.space.interfaces import _, ISpace

from cache import ContentTag
from interfaces import IRecentContentPortlet, IContentRecentContentPortlet
from zope.security.proxy import removeSecurityProxy


class RecentContentPortlet(object):
    interface.implements(IRecentContentPortlet)

    rssfeed = 'contents'
    cssclass = 'portlet-recent-content'
    noContentsMessage = _('No content has been created yet.')

    def __init__(self, context, request, view, manager):
        context = getSpace(context, getSite())

        super(RecentContentPortlet, self).__init__(context,request,view,manager)

    def getMoreLink(self):
        return None

    def extraParameters(self):
        return {'typeType': {'any_of': ('Portal type',)}}

    def listContents(self):
        context = self.context
        request = self.request
        catalog = getUtility(ICatalog)
        ids = getUtility(IIntIds)
        formatter = getFormatter(request, 'humanDatetime', 'medium')

        query = {'traversablePath': {'any_of':(context,)},
                 'sort_order': 'reverse',
                 'sort_on': 'modified',
                 'isDraft': {'any_of': (False,)}}

        if '__all__' in self.types:
            query['typeType']={'any_of': ('Portal type',)}
        else:
            query['type']={'any_of': self.types}

        try:
            local_context = self.manager.view.maincontext
        except AttributeError:
            local_context = context

        if self.spaceMode == 2:
            query['contentSpace'] = {'any_of': [ids.queryId(removeSecurityProxy(getSpace(local_context)))] }
            del query['traversablePath']
        elif self.spaceMode == 3:
            query['traversablePath'] = {'any_of':(getSpace(local_context),)}

        query.update(self.extraParameters())

        docs = []
        for document in catalog.searchResults(**query)[:self.number]:
            view = queryMultiAdapter((document, request), IContentViewView)
            if view is not None:
                url = '%s/%s'%(absoluteURL(document, request), view.name)
            else:
                url = '%s/'%absoluteURL(document, request)

            space = getSpace(document, context)
            item = IItem(document, None)

            docs.append({'url': url,
                         'title': getattr(item, 'title', document.__name__),
                         'description': getattr(item, 'description', u''),
                         'date': formatter.format(IDCTimes(document).modified),
                         'icon': queryMultiAdapter(
                                   (document, request), name='zmi_icon'),
                         'space': space.title,
                         'spacedescription': space.description,
                         'spaceurl': '%s/'%absoluteURL(space, request),
                         'content': document,
                         })
        return docs

    @cache(PortletId(), PortletModificationTag, Principal, ContentTag)
    def updateAndRender(self):
        self.update()
        if self.isAvailable():
            return self.render()
        else:
            return u''


class ContentRecentContentPortlet(RecentContentPortlet):
    interface.implements(IContentRecentContentPortlet)

    cssclass = u''

    def listContents(self):
        data = super(ContentRecentContentPortlet, self).listContents()

        request = self.request

        for item in data:
            content = item['content']

            owner = getattr(IOwnership(content, None), 'owner', None)
            if owner is not None:
                profile = IPersonalProfile(owner)
                item['avatar'] = profile.avatarUrl(request)
                item['author'] = profile.title

                space = profile.space
                if space is not None:
                    item['profile'] = '%s/'%absoluteURL(space, request)
                else:
                    item['profile'] = u''
            else:
                item['avatar'] = u''
                item['author'] = u''
                item['profile'] = u''

        return data

    @cache(PortletId(), PortletModificationTag, Principal, ContentTag)
    def updateAndRender(self):
        self.update()
        if self.isAvailable():
            return self.render()
        else:
            return u''
