from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory 

from osha.dynamicpressroom.tests.base import ZentraliseTestCase

class TestVocabularies(ZentraliseTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory('Folder', 'press-contacts')
        folder = getattr(self.portal, 'press-contacts')
        folder.invokeFactory('PressContact', 'john-smith')
        folder.invokeFactory('PressContact', 'mike-morriss')

    def testSinToolKeysVocabulary(self):
        vocab = getUtility(IVocabularyFactory, name="osha.dynamicpressroom.SinToolKeyVocabulary")
        terms = [t.value for t in vocab(self.portal)._terms]
        rss_terms = [
                'cmsinfo', 'freshmeat', 'oscom', 
                'pypi', 'pyware', 'slashdot', 
                'zdispaches', 'zltop', 'znewb', 
                'zonews', 'zopelabs', 'zoproducts',
                ]
        self.assertEquals(terms, rss_terms)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestVocabularies))
    return suite

