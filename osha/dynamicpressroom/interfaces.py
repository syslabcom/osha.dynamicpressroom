from zope import interface
from zope.app.content.interfaces import IContentType


class IPressRoom(interface.Interface):
    """A new MindMap File subtype."""

interface.alsoProvides(IPressRoom, IContentType)
