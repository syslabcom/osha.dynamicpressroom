Introduction
============

This product adds aggregation features to the PressRoom content type supplied
by Products.PressRoom.

http://plone.org/products/pressroom 

The goal is to provide a view on a pressroom where not only is the
content of itself is presented, but also content from a global pressroom.

You could use a normal Topic/Collection to achieve this, but in sites with
multiple translations, Collections become a bit of a pain.


How it works (Doc Tests):
=========================

We create the global PressRoom from which our sattelite pressrooms will pull
data and present it in their own contexts.

    >>> self.loginAsPortalOwner()
    >>> self.folder.invokeFactory('PressRoom', 'global-press')
    'global-press'
    >>> global_press = self.folder._getOb('global-press')

Lets see what was created automatically inside our shiny new pressroom:

    >>> global_press.objectIds()
     ['press-releases', 'press-clips', 'press-contacts']

Let's create some press releases:

    >>> press_releases = getattr(global_press, 'press-releases')
    >>> press_releases.invokeFactory('PressRelease', 'global-press-release1')
    'global-press-release1'

    >>> press_releases.invokeFactory('PressRelease', 'global-press-release2')
    'global-press-release2'

Now we create some clips:

    >>> press_clips = getattr(global_press, 'press-clips')
    >>> press_clips.invokeFactory('PressClip', 'global-press-clip1')
    'global-press-clip1'

    >>> press_clips.invokeFactory('PressClip', 'global-press-clip2')
    'global-press-clip2'

And lastly we create some Press Contacts:

    >>> press_contacts = getattr(global_press, 'press-contacts')
    >>> press_contacts.invokeFactory('PressContact', 'global-press-contact1')
    'global-press-contact1'

    >>> global_press_contact1 = getattr(press_contacts, 'global-press-contact1')

    >>> press_contacts.invokeFactory('PressContact', 'global-press-contact2')
    'global-press-contact2'

    >>> global_press_contact2 = getattr(press_contacts, 'global-press-contact2')


Now we create a sattelite pressroom, that will pull data from the global
pressroom and display it within its own context:

Usually this 'local' pressroom, will be located somewhere else in the site, so
we create it inside a subfolder.

    >>> self.folder.invokeFactory('Folder', 'local-folder')
    'local-folder'

    >>> local_folder = getattr(self.folder, 'local-folder')

    >>> local_folder.invokeFactory('PressRoom', 'local-press')
    'local-press'

    >>> local_press = local_folder._getOb('local-press')


To be able to use our local pressroom as a 'dynamic pressroom', we first need
to subtype it.

    >>> from p4a.subtyper.interfaces import ISubtyper
    >>> from zope import component
    >>> subtyper = component.getUtility(ISubtyper)    
    >>> subtyper.change_type(local_press, 'osha.dynamicpressroom.dynamicpressroom')


We now modify the aggregation settings.

First we must tell our local pressroom, where the global pressroom is. I.e from
where must it fetch additional pressroom stuff:

    >>> field_globalPressRoom = local_press.Schema().getField('globalPressRoom')
    >>> field_globalPressRoom.set(local_press, global_press)
    >>> field_globalPressRoom.get(local_press)
     <PressRoom at .../global-press>

Then we set the the Press Contacts from the global pressroom:

    >>> field_pressContacts = local_press.Schema().getField('pressContacts')
    >>> field_pressContacts.set(local_press, [global_press_contact1, global_press_contact2])
    >>> field_pressContacts.get(local_press)
     [<PressContact at .../global-press-contact1>, <PressContact at .../global-press-contact2>]

Now we set the the Press Contacts from the global pressroom:

    >>> field_pressContacts = local_press.Schema().getField('pressContacts')
    >>> field_pressContacts.set(local_press, [global_press_contact1, global_press_contact2])
    >>> field_pressContacts.get(local_press)
     [<PressContact at .../global-press-contact1>, <PressContact at .../global-press-contact2>]

