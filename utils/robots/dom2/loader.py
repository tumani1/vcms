# coding: utf-8
import glob
import json
import os
import subprocess
import urllib
from xml.dom.minidom import parseString
from bs4 import BeautifulSoup
import requests
from crawler.dom2_fizruk_robots.dom2.parser_supp import get_episods_for_page, get_episode_quick_info
from crawler.locrobots.save_util import save_loaded_data_to_file

__author__ = 'vladimir'

URL_LOAD = 'http://dom2.ru/videos/page/{}'
URL_OLD_ACTRORS_LOAD = 'http://dom2.ru/heroes/old/page/{}'


# Загрузка страницы с dom2.ru


def load_pages():
    pages = []
    page_index = 0
    while True:
        page_file = load_one_page(page_index)

        if not page_file:
            break
        page_index += 1
        pages = pages + [page_file]
    return pages


def load_one_page(page_index):
    file_name = None
    json_path = 'saved_pages/dom2/'
    if not os.path.exists(json_path+'page_{}.json'.format(page_index)):
        page_link = URL_LOAD.format(page_index)
        response = requests.get(page_link)
        prepared_json = generate_json(response.content, page_link)
        if prepared_json:
            file_name = save_loaded_data_to_file(prepared_json, 'page_{}'.format(page_index), 'dom2')
        print "loaded page", page_index
    else:
        file_name = json_path+'page_{}.json'.format(page_index)
        print "page already has been loaded", page_index
    return file_name


def generate_json(page_content, page_link):
    beatiful_soup = BeautifulSoup(page_content)
    if len(beatiful_soup.findAll('div', { "class" : "item first"})) > 0 or len(beatiful_soup.findAll('div', {"id": "movieContainer"}))>0 \
            or len(beatiful_soup.findAll('div', { "class" : "phtgal"})) > 0:
        return {'html': page_content, 'url': page_link}
    else:
        return None


def actors_generate_json(page_content, page_link):
    beatiful_soup = BeautifulSoup(page_content)
    if len(beatiful_soup.findAll('td',{"class": "descr"})) > 0:
        return {'html': page_content, 'url': page_link}
    else:
        return None



def load_video_info_page(link, label):
    file_name = None
    json_path = 'saved_pages/dom2/'
    if not os.path.exists(json_path+u'video_info_page_{}.json'.format(label)):
        response = requests.get(link)
        prepared_json = generate_json(response.content, link)
        if prepared_json:
            file_name = save_loaded_data_to_file(prepared_json, u'video_info_page_{}'.format(label), 'dom2')
        print "loaded info page", label
    else:
        file_name = json_path+u'video_info_page_{}.json'.format(label)
        print "page already has been loaded", label
    return file_name


def load_old_actors_pages():
    pages = []
    page_index = 0
    while True:
        page_file = load_one_old_actors_pages(page_index)
        if not page_file:
            break
        page_index += 1
        pages = pages + [page_file]
    return pages


def load_current_actors_page():
    file_name = None
    page_link = 'http://dom2.ru/heroes'
    response = requests.get(page_link)
    prepared_json = actors_generate_json(response.content, page_link)
    if prepared_json:
        file_name = save_loaded_data_to_file(prepared_json, 'page_current_actors', 'dom2')
    return file_name


def load_one_old_actors_pages(page_index):
    file_name = None
    page_link = URL_OLD_ACTRORS_LOAD.format(page_index)
    response = requests.get(page_link)
    prepared_json = actors_generate_json(response.content, page_link)
    if prepared_json:
        file_name = save_loaded_data_to_file(prepared_json, 'page_old_actors_{}'.format(page_index), 'dom2')
    return file_name


def load_all_videoinfo_pages():
    pages = []
    pages = load_pages()
    for page in pages:
        opned_page = open(page)
        json_page = json.load(opned_page)
        beatiful_soup = BeautifulSoup(json_page['html'])
        episods = get_episods_for_page(beatiful_soup)
        for episode in episods:
            try:
                episod_quick_info = get_episode_quick_info(episode)
                video_info_page = load_video_info_page(episod_quick_info['video_info_page_url'], episod_quick_info['label'])
            except Exception, e:
                import traceback
                traceback.print_exc()
                print "videoinfo page does not load:", e.message
                continue


def download_dom2_videos():
    uploads_path = 'static/upload/Dom2/'
    if not os.path.exists(uploads_path):
        os.makedirs(uploads_path)
    json_path = 'saved_pages/dom2/'
    files = os.listdir(json_path)
    for file_name in files:
        try:
            trimmed_fname = file_name.split('.')[0]
            if os.path.exists(uploads_path + trimmed_fname + ".flv"):
                print "Skipped ", trimmed_fname
            if not os.path.exists(uploads_path + trimmed_fname + ".flv") and ('video_info_page' in file_name):
                print "I'm trying to download file ", trimmed_fname
                with open(json_path + file_name) as current_file:
                    json_page = json.load(current_file)
                    beatiful_soup = BeautifulSoup(json_page['html'])
                    main = beatiful_soup.find('table', {"class": "all"})
                    middle_td = main.find('td', {"class": "middle"})
                    table = middle_td.find('table', {"class": "bottom-bg"})
                    div = table.find('div', {"class": "content max-width"})
                    div_content = div.find('div', {"id": "the_content"})
                    div_the_content2 = div_content.find('div', {"id": "the_content2"})
                    inner_table = div_the_content2.find('table', {"class": "center-content"})
                    left_column = inner_table.find('td', {"class": "left-column"})
                    div_persent_pad = left_column.find('div', {"class": "percent-pad"})
                    center_table = div_persent_pad.find('table', {"class": "center-subcontent"})
                    left_slice = center_table.find('td', {"class": "left-slice"})
                    div_big_panel = left_slice.find('div', {"class": "b-bigPanel"})
                    div_big_panel_content = div_big_panel.find('div', {"class": "b-bigPanel__content"})
                    photo_panel_table = div_big_panel_content.find('table', {"class": "photo-panel all-height"})
                    iframe = photo_panel_table.find('iframe')
                    video_link = iframe['src']
                    #print "Video link:", video_link
                    if 'rutube.ru' in video_link:
                        id = get_id_by_embedded_link(video_link)
                        download_video_by_id(id, trimmed_fname)
                    else:
                        video_id = get_video_id_by_page_url(json_page['url'])
                        video_url = generate_video_url(video_id)
                        file_link = get_video_file_link(video_url)
                        save_flv_to_disk(file_link, trimmed_fname)
        except Exception, e:
            print "Error appears", e.message
            print "Not successful for", file_name
            continue

    for fl in glob.glob("*Frag*"):
        os.remove(fl)



def save_flv_to_disk(file_link, name):
    uploads_path = 'static/upload/Dom2/'
    file = urllib.URLopener()
    try:
        file.retrieve(file_link, uploads_path + name + ".flv")
        print "Downloading from Dom2 server finished"
    except:
        file.close()
        if os.path.exists(uploads_path + name + ".flv"):
            os.remove(uploads_path + name + ".flv")
        print "#Downloading not finished! Content Too Short Error or 404. File deleted"


def get_video_id_by_page_url(page_url):
    return page_url.split('/')[4].split('?')[0]


def generate_video_url(id):
    return 'http://dom2.ru/video/player?id=' + id


def get_video_file_link(video_url):
    r = requests.get(video_url)
    dom = parseString(r.content)
    root = dom.documentElement
    atr = root.getAttributeNode('video')
    flv = atr.nodeValue
    full_flv_link = 'http://dom2.ru' + flv
    return full_flv_link


def download_video_by_id(id, file_name):
    BASE_PATH = os.path.join('static/upload/', 'Dom2/')
    manifest_root_link = 'http://rutube.ru/api/play/options/{}/?format=xml'.format(id)
    try:
        manifest_txt = requests.get(manifest_root_link)
        f4link =  get_manifest_f4_link(manifest_txt.content)
        bashCommand = "php crawler/dom2_fizruk_robots/AdobeHDS.php --manifest \"{}\" --outfile \"{}.mp4\"".format(f4link, BASE_PATH + file_name)
        process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        #print out
        print "Downloading from rutube finished"
    except:
        if os.path.exists(BASE_PATH + file_name + ".flv"):
            os.remove(BASE_PATH + file_name + ".flv")
        print "#Downloading not finished! File deleted"


def get_manifest_f4_link(xml_root_file):
    dom = parseString(xml_root_file)
    video_manifest_default_link = dom.getElementsByTagName('default')
    element_lnk = video_manifest_default_link.item(0).firstChild.nodeValue
    #print element_lnk
    return element_lnk


def get_id_by_link(link):
    #print link
    return link


def get_id_by_embedded_link(embedded_link):
    r = requests.get(embedded_link)
    soup = BeautifulSoup(r.content)
    rutube_link = soup.findAll('link')[0]
    #print "Rutube link:",rutube_link
    if 'private' in rutube_link:
        link = str(rutube_link).split('/')[5]
    else:
        link = str(rutube_link).split('/')[4]
    #print "ID:", link
    return link