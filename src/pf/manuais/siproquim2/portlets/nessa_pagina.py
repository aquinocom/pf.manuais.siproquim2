# -*- coding: utf-8 -*-

from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope.site.hooks import getSite

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.portlets import base

from bs4 import BeautifulSoup


class INessaPaginaPortlet(IPortletDataProvider):

    pass


class Assignment(base.Assignment):
    implements(INessaPaginaPortlet)

    @property
    def title(self):
        return _(u"PF: âncoras nessa página")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('nessa_pagina.pt')

    title = _('box_nessa_pagina', default=u"Nessa página")

    def getAncorasPortlet(self):
        
        if self.context.Type() == 'Page':
            html_getText = self.context.getText()
        else:
            html_getText = ''
        soup = BeautifulSoup(html_getText, "lxml")
        links = []
        # soup.find('a').next
        
        for i in soup.find_all("a"):
            # import pdb; pdb.set_trace()
            try:
                dic = {
                    'id': i['name'],
                    'nome': i.next,
                }
                
                links.append(dic)
            except Exception as e:
                pass
        return links


class AddForm(base.NullAddForm):
    form_fields = form.Fields(INessaPaginaPortlet)
    label = _(u"Add PF: Nessa página Portlet")
    description = _(u"Portlet para apresentar as ancoras da pagina")

    def create(self):
        return Assignment()
