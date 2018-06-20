# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interfaces import IATNewsItem
from plone.memoize.instance import memoize
from DateTime import DateTime


class PaginaInicialView(BrowserView):
    """ view list news
    """

    # __call__ = ViewPageTemplateFile('templates/')

    @memoize
    def dateFormat(self, data):
        """Retorna a data formatada.
        """
        try:
            return DateTime(data).strftime('%d/%m/%Y')
        except:
            return False

    @memoize
    def results(self, path):
        """Retorna o resultado de uma consulta no catalog.
        """
        catalog = getToolByName(self, 'portal_catalog')
        news = catalog(object_provides=IATNewsItem.__identifier__,
                               path=path,
                               sort_on='effective',
                               sort_order='reverse')
        return news

    @memoize
    def listNews(self, news):
        """Retorna um dicionário com os dados
        """
        dicNews = {}
        for obj in news:
            try:
                try:
                    date = obj.effective.strftime('%Y/%m/%d')
                    time = DateTime(obj.effective).strftime('%Hh%M')
                except:
                    date = obj.created.strftime('%Y/%m/%d')
                    time = DateTime(obj.created).strftime('%Hh%M')
                data_news = dict(title=obj.Title,
                                 time=time,
                                 url=obj.getURL(),)
                if date not in dicNews:
                    dicNews[date] = [data_news]
                else:
                    dicNews[date].append(data_news)
            except:
                pass
        return dicNews
