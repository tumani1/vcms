import os
import urllib2


def save_avatar_to_file(link, name, token):
    file_name = None
    directory = 'upload'

    if not os.path.exists(directory):
        os.makedirs(directory)

    directory = directory + '/' + token
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        img = urllib2.urlopen(link)
        with open(directory + '/' + name + '.jpg', 'wb') as localFile:
            localFile.write(img.read())
        file_name = name + '.jpg'
    except Exception, e:
        print e.message
        print "Avatar saving failed"
    return file_name