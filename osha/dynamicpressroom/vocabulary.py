from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from zope.app.component.hooks import getSite

from Products.CMFCore.utils import getToolByName


class SinToolKeyVocabulary(object):
    """Vocabulary factory returning all available keys in CMFSin's
    sin_tool.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        sin = getToolByName(site, 'sin_tool', None)
        items = []
        if sin is not None:
            for c in sin.Channels():
                items.append(SimpleTerm(c.id, c.id, c.id))

        return SimpleVocabulary(items)

SinToolKeyVocabulary = SinToolKeyVocabulary()
