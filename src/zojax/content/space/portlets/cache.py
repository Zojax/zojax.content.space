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
from zope import component
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zojax.cache.tag import ContextTag
from zojax.content.type.interfaces import \
    IContent, IPortalType, IContentType, IDraftedContent

ContentTag = ContextTag('zojax.content.space.recencontent')


@component.adapter(IContent, IObjectModifiedEvent)
def contentHandler(ob, ev):
    ct = IContentType(ob, None)
    if IPortalType.providedBy(ct) and not IDraftedContent.providedBy(ob):
        try:
            ContentTag.update(ob)
        except TypeError:
            pass
