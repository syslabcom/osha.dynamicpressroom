import unittest2 as unittest

from osha.dynamicpressroom.tests.base import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class TestVocabularies(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        # Login as manager
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.portal.invokeFactory('Folder', 'press-contacts')
        folder = getattr(self.portal, 'press-contacts')
        folder.invokeFactory('PressContact', 'john-smith')
        folder.invokeFactory('PressContact', 'mike-morriss')

    def testSinToolKeysVocabulary(self):
        # XXX: This test is failing because we don't have Products.CMFSin
        # installed
        vocab = getUtility(IVocabularyFactory,
                name="osha.dynamicpressroom.SinToolKeyVocabulary")
        terms = [t.value for t in vocab(self.portal)._terms]
        rss_terms = [
            'cmsinfo', 'freshmeat', 'oscom',
            'pypi', 'pyware', 'slashdot',
            'zdispaches', 'zltop', 'znewb',
            'zonews', 'zopelabs', 'zoproducts',
        ]
        self.assertEquals(terms, rss_terms)


def test_suite():
    """This sets up a test suite that actually runs the tests in
    the class(es) above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
