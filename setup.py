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
"""Setup for zojax.content.space package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version='0'


setup(name='zojax.content.space',
      version=version,
      description="Content space.",
      long_description=(
          'Detailed Documentation\n' +
          '======================\n'
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      author='Nikolay Kim',
      author_email='fafhrd91@gmail.com',
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['zojax', 'zojax.content'],
      install_requires = ['setuptools',
                          'zope.interface',
                          'zope.component',
                          'zope.schema',
                          'zope.proxy',
                          'zope.location',
                          'zope.security',
                          'zope.securitypolicy',
                          'zope.i18n',
                          'zope.i18nmessageid',
                          'zope.publisher',
                          'zope.traversing',
                          'zope.app.security',
                          'zope.app.component',
                          'zope.app.intid',
                          'zope.lifecycleevent',

                          'zojax.layout',
                          'zojax.layoutform',
                          'zojax.portlet',
                          'zojax.content.type',
                          'zojax.content.feeds',
                          'zojax.content.forms',
                          'zojax.content.draft',
                          'zojax.content.actions',
                          'zojax.content.table',
                          'zojax.content.permissions',
                          'zojax.principal.profile',
                          'zojax.widget.checkbox',
                          'zojax.statusmessage',
                          'zojax.table',
                          'zojax.cache',
                          ],
      extras_require = dict(test=['zope.app.testing',
                                  'zope.app.zcmlfiles',
                                  'zope.securitypolicy',
                                  'zope.testing',
                                  'zope.testbrowser',
                                  'zojax.autoinclude',
                                  'zojax.security',
                                  'zojax.personal.space',
                                  'zojax.personal.content',
                                  'zojax.content.browser',
                                  'zope.app.file',
                                  ]),
      include_package_data = True,
      zip_safe = False
      )
