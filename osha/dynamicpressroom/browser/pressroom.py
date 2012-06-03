from zope.interface import implements

from Acquisition import aq_inner
from Acquisition import aq_parent

from Products.ATContentTypes.interface.document import IATDocument
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

from osha.dynamicpressroom.browser.interfaces import IPressRoomView


class PressRoom(BrowserView):
    implements(IPressRoomView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.result = []

    def _render_cachekey(method, self):
        return ('meltwater')

    def getContext(self):
        context = aq_inner(self.context)
        # if dynamic-pressroom was used on a Document, get the parent-folder
        if IATDocument.providedBy(context):
            context = aq_parent(context)
        if hasattr(context, 'isCanonical') and not context.isCanonical():
            context = context.getCanonical()
        return context

    #@ram.cache(_render_cachekey)
    def get_feed(self):
        context = self.getContext()
        keys = context.Schema().getField('RSSKeys').get(context)
        try:
            sin = getToolByName(context, 'sin_tool')
        except AttributeError:
            return []
        rows = []
        for k in keys:
            rows += sin.sin(k, max_size=2)
        return rows

    def has_global_pressroom(self):
        context = self.getContext()
        if context.Schema().getField('globalPressRoom').get(context):
            return True
        return False

    #@ram.cache(_render_cachekey)
    def get_press_contacts(self):
        context = self.getContext()
        return context.Schema().getField('pressContacts').get(context)

    def get_press_subfolder(self, folder):
        context = self.getContext()
        field = context.Schema().getField('globalPressRoom')
        if field.get(context):
            return field.get(context)._getOb(folder)
        else:
            return None

    def get_press_releases(self):
        context = self.getContext()
        cat = getToolByName(context, 'portal_catalog')
        sf = self.get_press_subfolder('press-releases')
        path = '/'.join(sf.getPhysicalPath())
        q = {
            'portal_type': 'PressRelease',
            'path': path,
            'sort_on': 'Date',
            'sort_order': 'reverse',
        }
        keywords = context.Schema().getField('filteringKeywords').get(context)
        if keywords:
            q['Subject'] = keywords
        return cat(q)

    def get_articles(self):
        context = self.getContext()
        cat = getToolByName(context, 'portal_catalog')
        sf = self.get_press_subfolder('articles')
        path = '/'.join(sf.getPhysicalPath())
        q = {
            'path': path,
            'sort_on': 'effective',
            'sort_order': 'reverse',
        }
        keywords = context.Schema().getField('filteringKeywords').get(context)
        if keywords:
            q['Subject'] = keywords

        return [r for r in cat(q) if r.UID != sf.UID()]

    def get_audiovisual(self):
        context = self.getContext()
        cat = getToolByName(context, 'portal_catalog')
        sf = self.get_press_subfolder('photos')
        path = '/'.join(sf.getPhysicalPath())
        q = {'path': path}
        keywords = context.Schema().getField('filteringKeywords').get(context)
        if keywords:
            q['Subject'] = keywords

        return [r for r in cat(q) if r.UID != sf.UID()]
