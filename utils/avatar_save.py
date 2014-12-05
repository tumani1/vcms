import os
import urllib


def save_avatar_to_file(link, name, subdirectory):
    directory = 'upload'

    if not os.path.exists(directory):
        os.makedirs(directory)

    directory = directory + '/' + subdirectory
    if not os.path.exists(directory):
        os.makedirs(directory)
    ext = os.path.splitext(link)[1]
    if not ext:
        photo_file = urllib.urlopen(link)
        ext = '.' + photo_file.headers.subtype

    try:
        urllib.urlretrieve(link, directory + '/' + name + ext)

    except Exception, e:
        print e.message
        print "Avatar saving failed"
    return name