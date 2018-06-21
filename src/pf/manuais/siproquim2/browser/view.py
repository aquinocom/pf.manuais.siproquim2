# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interfaces import IATFolder
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
    def getTopicosPopulares(self):
        """Retorna o resultado de uma consulta no catalog.
        """
        # import pdb; pdb.set_trace()
        catalog = getToolByName(self, 'portal_catalog')
        categoria = "Tópicos populares"
        folders = catalog(Subject = categoria)
        return folders

    @memoize
    def getFolders(self):
        """Retorna o resultado de uma consulta no catalog.
        """
        catalog = getToolByName(self, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        folders = catalog(object_provides=IATFolder.__identifier__,
                          path={'query':path, 'depth':1},
                          sort_on='getObjPositionInParent',

                         )
        return folders

    @memoize
    def getFolderItens(self, path):
        """Retorna o resultado de uma consulta no catalog.
        """
        # import pdb; pdb.set_trace()
        catalog = getToolByName(self, 'portal_catalog')
        folders = catalog(path={'query':path, 'depth':1},
                          sort_on='getObjPositionInParent',
                         )
        return folders

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
