#coding: utf-8
import json
import os
import subprocess
from bs4 import BeautifulSoup
import requests
from xml.dom.minidom import parse, parseString, Element
from utils.robots.dom2.loader import remove_frag_files
from utils.robots.support_functions import save_loaded_data_to_file

__author__ = 'vladimir'

URL_LOAD = 'http://fizruk.tnt-online.ru/video.html'
SEASONS_COUNT = 2

def get_info_pages():
    i=1
    all_pages = []
    while(True):
        response = requests.get(URL_LOAD+'?season={}'.format(i))
        if i > SEASONS_COUNT:
            break
        print "Processing season {}".format(i)
        beatiful_soup = BeautifulSoup(response.content)
        season_pages = get_season_pages(i, beatiful_soup)
        all_pages = all_pages + season_pages
        i += 1
    return all_pages, len(all_pages)


def get_season_pages(season_num, beatiful_soup):
    pages = []
    tvbl_s = beatiful_soup.findAll('div', { "class" : "tvbl"})
    for one_tvbl in tvbl_s:
        text = one_tvbl.find('div', { "class" : "text"})
        h4 = text.find('h4')
        a = h4.find('a')
        label = a.text.encode('utf-8')
        str(label.split('№')[1].split('.')[0])
        s_label =  "S_" + str(season_num) + "_video_" + str(label.split('№')[1].split('.')[0])
        link = 'http://fizruk.tnt-online.ru/' + a['href']
        info_page_response = requests.get(link)
        prepared_json = generate_json(info_page_response.content, link)
        if prepared_json:
            file_name = save_loaded_data_to_file(prepared_json, s_label, 'fizruk')
            pages = pages + [file_name]
    return pages


def generate_json(page_content, page_link):
    return {'html': page_content, 'url': page_link}


def download_fizruk_videos(uploads_path='static/upload/Fizruk/', json_path='saved_pages/fizruk/'):
    files = os.listdir(json_path)
    for file_name in files:
        trimmed_fname = file_name.split('.')[0]
        if not os.path.exists(uploads_path + trimmed_fname + ".flv"):
            print 'File', trimmed_fname, 'will be downloaded'
            with open(json_path + file_name) as current_file:
                json_page = json.load(current_file)
                beatiful_soup = BeautifulSoup(json_page['html'])
                all = beatiful_soup.find('div', { "id" : "all"})
                content = all.find('div', { "id" : "content"})
                center_block = content.find('div', { "id" : "center-block"})
                video_player_now = center_block.find('div', { "id" : "video-player-now"})
                iframe = video_player_now.find('iframe')
                video_link = iframe['src']
                id = get_id_by_embedded_link(video_link)
                download_video_by_id(id, trimmed_fname)


def download_video_by_id(id, file_name):
    BASE_PATH = os.path.join('static/upload/', 'Fizruk/')
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)
    try:
        manifest_root_link = 'http://rutube.ru/api/play/options/{}/?format=xml'.format(id)
        manifest_txt = requests.get(manifest_root_link)
        f4link = get_manifest_f4_link(manifest_txt.content)
        bashCommand = "php utils/robots/AdobeHDS.php --manifest \"{}\" --outfile \"{}.mp4\"".format(f4link, BASE_PATH + file_name)
        process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print out
    except:
        if os.path.exists(BASE_PATH + file_name + ".flv"):
            os.remove(BASE_PATH + file_name + ".flv")
        print "#Downloading not finished! File deleted"
    remove_frag_files()


def get_manifest_f4_link(xml_root_file):
    dom = parseString(xml_root_file)
    video_manifest_default_link = dom.getElementsByTagName('default')
    element_lnk = video_manifest_default_link.item(0).firstChild.nodeValue
    return element_lnk


def get_id_by_embedded_link(embedded_link):
    r = requests.get(embedded_link)
    soup = BeautifulSoup(r.content)
    rutube_link = soup.findAll('link')[0]
    link = str(rutube_link).split('/')[4]
    return link