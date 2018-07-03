# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interfaces import IATFolder
from plone.memoize.instance import memoize
from DateTime import DateTime

from bs4 import BeautifulSoup
from zope.site.hooks import getSite
from zope.component import queryUtility
import logging
from plone.i18n.normalizer.interfaces import IIDNormalizer
from DateTime import DateTime
from plone import api
from Products.CMFPlone.utils import _createObjectByType


class PaginaInicialView(BrowserView):
    """ view list news
    """

    # __call__ = ViewPageTemplateFile('templates/')
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.errors = {}
        self.url_sucess = self.context.absolute_url()

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
        
        catalog = getToolByName(self, 'portal_catalog')
        categoria = "Tópicos populares"
        folders = catalog(Subject = categoria, exclude_from_nav=False)
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
                          exclude_from_nav=False
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
                          exclude_from_nav=False
                         )
        return folders

    def getAncorasPortlet(self):
        
        if self.context.Type() == 'Page':
            html_getText = self.context.getText()
        else:
            html_getText = ''
        soup = BeautifulSoup(html_getText, "lxml")
        links = []
        for i in soup.find_all("a"):
            try:
                links.append(i['name'])
            except Exception as e:
                pass
        return links

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


class FeedbackAddForm(BrowserView):
    """ 
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.errors = {}
        self.url_sucess = self.context.absolute_url()

        if 'feedback_txt' in request.form:
            feedback_txt_conteudo = request.form['feedback_txt']
            request.set('feedback_txt', feedback_txt_conteudo)
            self.feedback_txt_conteudo = feedback_txt_conteudo


    def __call__(self):
        
        if 'form.feedback_comment' in self.request.form:

            return self.createFeedback(self.feedback_txt_conteudo)

        return self.index()

    @memoize
    def validateForm(self,feedback_txt_conteudo):

        if (feedback_txt_conteudo == ''):
            self.errors['feedback_txt'] = "O campo é obrigatório."

        # Check for errors
        if self.errors:
            self.utils.addPortalMessage("Corrija os erros.", type='error')
            return False
        else:
            return True

    def createFeedback(self, feedback_txt):
        """
        """
        log = logging.getLogger('createFeedback:')
        folder_conteudo = 'Feedback Admin'
        # import pdb; pdb.set_trace()
        try:
            pasta_manual = self.context.getPhysicalPath()[2]
        except:
            pasta_manual = self.context.id

        site = getSite()
        id_folder = queryUtility(IIDNormalizer).normalize(folder_conteudo)
        
        if not hasattr(site, id_folder):
            site.invokeFactory('Folder', id=id_folder, title=folder_conteudo)

        # folderFeedback = getattr(site, id_folder)
        folderFeedback = getattr(site, pasta_manual)

        paginaContext = {'titulo': self.context.Title(),
                         'uid': self.context.UID(),
                         'caminho': '/'.join(self.context.getPhysicalPath()), 
                         }

        zope_DT = DateTime() # this is now.
        python_dt = zope_DT.asdatetime()
        zope_DT = DateTime(python_dt)
        data_feedback = zope_DT.strftime('%d/%m/%Y-%H:%M')
        data_milisecond = zope_DT.strftime('%s')

        # import pdb; pdb.set_trace()

        titulo_content = 'Feedback '+ ' - ' + data_feedback + ' - ' + paginaContext['uid']
        id_content = 'feedback ' + data_feedback + '-' + data_milisecond
        id = queryUtility(IIDNormalizer).normalize(id_content)

        _createObjectByType('Document',
                            folderFeedback,
                            id,
                            title=titulo_content,
                            description=paginaContext['caminho'],
                            location=paginaContext['uid'],
                            creators='anonimo',
                            text=feedback_txt
                            )

        obj = getattr(folderFeedback, id)
        if obj:
            obj.setTitle(titulo_content)
            obj.setDescription(paginaContext['caminho']),
            obj.setText(feedback_txt),
            obj.setLocation(paginaContext['uid']),
            obj.setCreators('anonimo')
            obj.reindexObject()

        log.info(id)
        return self.request.response.redirect(self.url_sucess)
