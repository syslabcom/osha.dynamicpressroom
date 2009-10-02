from zope import interface
from p4a.subtyper.interfaces import IPortalTypedFolderishDescriptor
from osha.dynamicpressroom import interfaces

class DynamicPressRoomDescriptor(object):
    """ A Dynamic PressRoom descriptor for the PressRoom subtype.
    """
    interface.implements(IPortalTypedFolderishDescriptor)
    title = u'Dynamic Press Room'
    description = u''
    type_interface = interfaces.IPressRoom
    for_portal_type = 'PressRoom'


