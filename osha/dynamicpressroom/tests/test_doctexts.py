import unittest
import interlude
import zope.testing

from zope.app.testing import setup

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase.layer import PloneSite

from osha.dynamicpressroom.tests.base import ZentraliseTestCase


class TestCase(ZentraliseTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(test):
            pass

        @classmethod
        def tearDown(test):
            setup.placefulTearDown()

optionflags = (zope.testing.doctest.REPORT_ONLY_FIRST_FAILURE |
               zope.testing.doctest.ELLIPSIS |
               zope.testing.doctest.NORMALIZE_WHITESPACE
               )


def test_suite():
    return unittest.TestSuite((
        ztc.FunctionalDocFileSuite(
            'README.txt',
            package='osha.dynamicpressroom',
            test_class=TestCase,
            globs=dict(interact=interlude.interact),
            optionflags=optionflags
            ),
        ))
