# coding: utf-8
import json
import locale
import datetime
import os
import re
import shutil
import string
import urllib2
import subprocess
from models import Media
from utils.connection import get_session, mongo_connect
from utils.robots.locale_manager import convert_orig_month_name_to_lib
import traceback


def get_valid_date_for_str(date_str):
    locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
    res_date = None
    res_date_text = ''
    dates_parts = date_str.split(' ')
    if len(dates_parts) == 3:
        year = dates_parts[2]
    else:
        year = u'2014'
    if len(dates_parts) == 1:
        if date_str == u'Сегодня':
            day = datetime.datetime.now().day
        elif date_str == u'Вчера':
            day = datetime.date.fromordinal(datetime.date.today().toordinal()-1).day
        res_date_text = str(day) + ' ' + str(datetime.datetime.now().month) + ' ' + year
        res_date = datetime.datetime.strptime(res_date_text.encode("utf-8"), "%d %m %Y").date()
    else:
        try:
            res_date_text = dates_parts[0] + ' ' + convert_orig_month_name_to_lib(dates_parts[1]) + ' ' + year
            res_date = datetime.datetime.strptime(res_date_text.encode("utf-8"), "%d %B %Y").date()
        except ValueError, e:
            res_date_text = u'1' + ' ' + convert_orig_month_name_to_lib(dates_parts[1]) + ' ' + year
            res_date = datetime.datetime.strptime(res_date_text.encode("utf-8"), "%d %B %Y").date()
            print "Datetime converting error: ", dates_parts[0], convert_orig_month_name_to_lib(dates_parts[1]), year
        except Exception, e:
            print e.message
    return res_date


def save_loaded_data_to_file(loaded_json_data, file_name, sub_dir_name):
    saved_pages_directory = 'saved_pages'
    saved_file_name = file_name + '.json'
    try:
        if not os.path.exists(saved_pages_directory):
            os.makedirs(saved_pages_directory)
        site_dir = saved_pages_directory + '/' + sub_dir_name
        if not os.path.exists(site_dir):
            os.makedirs(site_dir)
        with open(site_dir + '/' + saved_file_name, 'w') as f:
            json.dump(loaded_json_data, f)

    except Exception, e:
        print "Saving failed with error:", traceback.print_exc()
        return None
    return site_dir + '/' + saved_file_name



def save_poster_to_file(link, name, directory='static/upload/dom2'):
    file_name = None
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        if 'dom2' not in link:
            link = 'http://dom2.ru'+link
        img = urllib2.urlopen(link)
        with open(directory + '/' + name + '.jpg', 'wb') as localFile:
            localFile.write(img.read())
        file_name = name + '.jpg'
    except Exception, e:
        print e.message
        print "Poster saving failed"
    return file_name


def format_dom_2_name_str(inp):
    return re.sub("\D", "", inp) + ' день'


def process_dom2_data_for_cdn(poster_dir = u'static/upload/dom2/', video_dir = u'static/upload/Dom2/'):
    session = get_session()
    mongo_connect()
    dom_2_files = u'cdn_dom2/'
    poster_name = u'poster.jpg'
    if not os.path.exists(dom_2_files):
        os.makedirs(dom_2_files)
    posters = os.listdir(poster_dir)
    videos = os.listdir(video_dir)
    media = session.query(Media).filter(Media.title.like('%день%')).all()
    for m in media:
        try:
            day_number = re.sub("\D", "", m.title)
            if not os.path.exists(dom_2_files + unicode(m.id) + u'/'):
                os.makedirs(dom_2_files + unicode(m.id) + u'/')
            for p in videos:
                if day_number in p:
                    bashCommand = u'avconv -y -threads 6 -i \"{inp}\" -codec copy \"{out}\"'.format(inp=video_dir + p,
                                                                                           out=dom_2_files + unicode(m.id) + u'/' + u'hd.mp4')
                    process = subprocess.Popen(bashCommand, shell=True)
                    process.communicate()
                    break

            for p in posters:
                if day_number in p:
                    shutil.move(poster_dir + p, dom_2_files+unicode(m.id) + u'/' + poster_name)
                    break
            if not os.path.exists(dom_2_files+ unicode(m.id) + u'/' + poster_name):
                    bashCommand = u'avconv -ss 300 -r 25 -i \"{mp4_video}\" -t 0.01 \"{poster_file}\"'.format(mp4_video=video_dir + m.title + u'.flv',
                                                                                           poster_file=dom_2_files + unicode(m.id) + u'/' + poster_name)
                    process = subprocess.Popen(bashCommand, shell=True)
                    process.communicate()

        except Exception, e:
            traceback.print_exc()
            continue