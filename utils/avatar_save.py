import os
import urllib


def save_avatar_to_file(link, name, subdirectory):
    directory = 'upload'

    if not os.path.exists(directory):
        os.makedirs(directory)

    directory = directory + '/' + subdirectory
    if not os.path.exists(directory):
        os.makedirs(directory)
    exp = link.split('.')
    exp_len = len(exp)
    exp = exp[exp_len-1]

    try:
        urllib.urlretrieve(link, directory + '/' + name + '.' + exp)

    except Exception, e:
        print e.message
        print "Avatar saving failed"
    return name