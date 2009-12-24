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
from zope.component import getAdapters
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zojax.content.space.interfaces import \
    ISpace, IWorkspaceFactory, IInactiveWorkspaceFactory
from zojax.content.space.utils import getSpace


class Workspaces(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        context = getSpace(context)

        wfs = []
        for name, wf in getAdapters((context,), IWorkspaceFactory):
            if not IInactiveWorkspaceFactory.providedBy(wf) and wf.isAvailable():
                term = SimpleTerm(name, name, wf.title)
                term.description = wf.description
                wfs.append((wf.weight, wf.title, term))

        wfs.sort()
        return SimpleVocabulary([term for _w, _t, term in wfs])


class EnabledWorkspaces(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        wfs = []
        for name, wf in getAdapters((context,), IWorkspaceFactory):
            if not IInactiveWorkspaceFactory.providedBy(wf) \
                    and context.isEnabled(wf):

                term = SimpleTerm(name, name, wf.title)
                term.description = wf.description
                wfs.append((wf.weight, wf.title, term))

        wfs.sort()
        return SimpleVocabulary([term for _w, _t, term in wfs])
