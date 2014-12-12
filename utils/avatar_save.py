import os
import urllib
from settings import SOCIAL_AVATAR_UPLOAD_DIR


def save_avatar_to_file(link, name, subdirectory):
    if not os.path.exists(SOCIAL_AVATAR_UPLOAD_DIR):
        os.makedirs(SOCIAL_AVATAR_UPLOAD_DIR)

    sub_dir = os.path.join(SOCIAL_AVATAR_UPLOAD_DIR, subdirectory)
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)
    ext = os.path.splitext(link)[1]
    if not ext:
        photo_file = urllib.urlopen(link)
        ext = '.' + photo_file.headers.subtype

    try:
        urllib.urlretrieve(link, sub_dir + '/' + name + ext)

    except Exception, e:
        print e.message
        print "Avatar saving failed"
    return name