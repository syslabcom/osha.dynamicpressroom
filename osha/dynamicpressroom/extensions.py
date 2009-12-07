from zope.interface import implements

from Products.Archetypes import atapi
from Products.Archetypes.utils import shasattr
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.field import ExtensionField

class ExtendedLinesField(ExtensionField, atapi.LinesField):
    """ """

class ExtendedReferenceField(ExtensionField, atapi.ReferenceField):
    """ """

    def get(self, instance, **kwargs):
        canonical = instance.getCanonical()
        canonical_refs = atapi.ReferenceField.get(self, canonical, **kwargs)
        if not canonical_refs:
            return canonical_refs

        portal_languages = getToolByName(instance, 'portal_languages')
        preflang = portal_languages.getPreferredLanguage()
        if not self.multiValued:
            o = canonical_refs
            if shasattr(o, 'getTranslation'):
                return o.getTranslation(preflang) or o.getCanonical()
            else: 
                return o.getCanonical()

        return [o.getTranslation(preflang) or o.getCanonical() for o in canonical_refs]


class DynamicPressRoom(object):
    """ Extends a PressRoom to get the aggregation settings fields """
    implements(IOrderableSchemaExtender)

    _fields = [
            ExtendedReferenceField('globalPressRoom',
                allowed_types = ('PressRoom',),
                relationship = 'aggregatesFrom',
                multiValued = False,
                isMetadata = True,
                languageIndependent = True,
                accessor='getGlobalPressRoom',
                mutator='setGlobalPressRoom',
                write_permission = permissions.ModifyPortalContent,
                schemata='aggregation',
                widget = ReferenceBrowserWidget(
                    label = _(u'label_global_pressroom', 
                            default=u'Reference to the global Press Room'),
                    description=_(u"The global pressroom's press releases, "
                                "articles, contacts and other data will be "
                                "presented in this pressroom as well."),
                    allow_search = True,
                    allow_browse = True,
                    show_indexes = False,
                    force_close_on_insert = True,
                    visible = {'edit' : 'visible', 'view' : 'invisible' },
                ),
            ),
            ExtendedLinesField('RSSKeys',
                languageIndependent = True,
                accessor='getRSSFeed',
                mutator='setRSSFeed',
                vocabulary_factory='osha.dynamicpressroom.SinToolKeyVocabulary',
                schemata='aggregation',
                widget = atapi.InAndOutWidget(
                    label = _(u'label_rss_feed', default=u'RSS Feed'),
                    description=_(
                        u"Choose the RSS profile for this PressRoom. "
                        "Profiles are created in the site control panel."
                        ),
                    visible = {'edit' : 'visible', 'view' : 'invisible' }
                ),
            ),
            ExtendedReferenceField('pressContacts',
                allowed_types = ('PressContact',),
                relationship = 'relatesTo',
                multiValued = True,
                isMetadata = True,
                languageIndependent = True,
                accessor='getPressContacts',
                mutator='setPressContacts',
                write_permission = permissions.ModifyPortalContent,
                schemata='aggregation',
                widget = ReferenceBrowserWidget(
                    label = _(u'label_pess_contacts', 
                            default=u'Reference to the Press Contacts'),
                    description=u'',
                    allow_search = True,
                    allow_browse = True,
                    show_indexes = False,
                    force_close_on_insert = True,
                    visible = {'edit' : 'visible', 'view' : 'invisible' }
                ),
            ),
            ExtendedLinesField('filteringKeywords',
                languageIndependent=True,
                accessor='getAuthor',
                mutator='setAuthor',   
                schemata='aggregation',
                widget=atapi.LinesWidget(
                    label = _(u'label_filtering_keywords', 
                            default=u'Filtering Keywords'),
                    description=_(
                        u'description_filtering_keywords', 
                        default=u'Add your keywords here, separate them with spaces.'
                    ),
                ),
            ),
            ]

    def __init__(self, context):
        """ init """
        self.context = context

    def getFields(self):
        """ get fields """
        return self._fields

    def getOrder(self, original):
        """ new order """
        aggregation = original.get('aggregation', [])
        aggregation.insert(0, 'RSSKeys')
        aggregation.insert(1, 'pressContacts')
        aggregation.insert(2, 'filteringKeywords')
        original['aggregation'] = aggregation
        return original
        

