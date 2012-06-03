from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import quickInstallProduct
from plone.testing import z2


class OshaDynamicPressRoom(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        #z2.installProduct(app, 'Products.CMFSin')
        z2.installProduct(app, 'Products.PressRoom')
        z2.installProduct(app, 'osha.dynamicpressroom')

        import Products.PressRoom
        self.loadZCML('configure.zcml', package=Products.PressRoom)

        import osha.dynamicpressroom
        self.loadZCML('configure.zcml', package=osha.dynamicpressroom)

    def setUpPloneSite(self, portal):
        #quickInstallProduct(portal, 'Products.CMFSin')
        quickInstallProduct(portal, 'Products.PressRoom')
        applyProfile(portal, 'osha.dynamicpressroom:default')

        # Login as manager and create a test folder
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'folder')

    def tearDownZope(self, app):
        #z2.uninstallProduct(app, 'Products.CMFSin')
        z2.uninstallProduct(app, 'Products.PressRoom')
        z2.uninstallProduct(app, 'osha.dynamicpressroom')


OSHA_DYNAMICPRESSROOM_FIXTURE = OshaDynamicPressRoom()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(OSHA_DYNAMICPRESSROOM_FIXTURE,),
    name="OshaDynamicPressRoom:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(OSHA_DYNAMICPRESSROOM_FIXTURE,),
    name="OshaDynamicPressRoom:Functional")
