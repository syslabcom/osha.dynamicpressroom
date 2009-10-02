from zope import component
from p4a.subtyper.interfaces import ISubtyper

# And external method that can be used to create dummy data to play/test with.

def run(self):
    portal = self.portal_url.getPortalObject()
    
    gpid = portal.invokeFactory('PressRoom', 'global-press')
    global_press = portal._getOb(gpid)
    global_press.setTitle('Global Press Room')

    press_releases = global_press._getOb('press-releases')
    for i in range(0, 10):
        prid = press_releases.invokeFactory('PressRelease', 'global-press-release%d' % i)
        pr = press_releases._getOb(prid)
        pr.setTitle('Global Press Release %d' % i)
        pr.setDescription('Description for Global Press Release %d' % i)

    press_clips = global_press._getOb('press-clips')
    for i in range(0, 10):
        prid = press_clips.invokeFactory('PressClip', 'global-press-clip%d' % i)
        pr = press_clips._getOb(prid)
        pr.setTitle('Global Press Clip %d' % i)
        pr.setDescription('Description for Global Press Clip %d' % i)

    press_contacts = global_press._getOb('press-contacts')
    for i in range(0, 10):
        prid = press_contacts.invokeFactory('PressContact', 'global-press-contact%d' % i)
        pr = press_contacts._getOb(prid)
        pr.setTitle('Global Press Contact %d' % i)
        pr.setDescription('Description for Global Press Contact %d' % i)


    aid = global_press.invokeFactory('Folder', 'articles')
    articles_folder = global_press._getOb(aid)
    articles_folder.setTitle('Articles and Interviews')
    
    aid = global_press.invokeFactory('Folder', 'photos')
    articles_folder = global_press._getOb(aid)
    articles_folder.setTitle('Images and Audiovisual')

    lpid = portal.invokeFactory('PressRoom', 'local-press')
    local_press = portal._getOb(lpid)
    local_press.setTitle('Local Press Room')

    subtyper = component.getUtility(ISubtyper)    
    subtyper.change_type(local_press, 'osha.dynamicpressroom.dynamicpressroom')

    press_releases = local_press._getOb('press-releases')
    for i in range(0, 3):
        prid = press_releases.invokeFactory('PressRelease', 'local-press-release%d' % i)
        pr = press_releases._getOb(prid)
        pr.setTitle('Local Press Release %d' % i)
        pr.setDescription('Description for Local Press Release %d' % i)

    press_clips = local_press._getOb('press-clips')
    for i in range(0, 3):
        prid = press_clips.invokeFactory('PressClip', 'local-press-clip%d' % i)
        pr = press_clips._getOb(prid)
        pr.setTitle('Local Press Clip %d' % i)
        pr.setDescription('Description for Local Press Clip %d' % i)

    press_contacts = local_press._getOb('press-contacts')
    for i in range(0, 3):
        prid = press_contacts.invokeFactory('PressContact', 'local-press-contact%d' % i)
        pr = press_contacts._getOb(prid)
        pr.setTitle('Local Press Contact %d' % i)
        pr.setDescription('Description for Local Press Contact %d' % i)

    return 'Finished'



