# coding: utf-8
import os
import urllib2
from utils.robots.support_functions import save_poster_to_file


def get_episods_for_page(soup):
    div_big_panel_content = get_b_big_panel_content_div(soup)
    div_photos = div_big_panel_content.find('div', {"class": "photos"})
    div_items = div_photos.findAll('div', {"class": "item first"})
    div_items = div_items + div_photos.findAll('div', {"class": "item "})
    return div_items


def get_episode_quick_info(episode):
    quick_info = {
        'label': '',
        'video_info_page_url': '',
        'poster': '',
    }

    a_tag = episode.find('a', {"class": "imgBox link no-select"})

    quick_info['label'] = unicode(episode.find('div', {"class": "photo-list-title"}).find('a').contents[0])
    quick_info['video_info_page_url'] = 'http://dom2.ru'+a_tag['href']
    img = a_tag.find('img')
    if img:
        poster_link = img['src']
        quick_info['poster'] = save_poster_to_file(poster_link, quick_info['label'])
    return quick_info

def get_b_big_panel_content_div(soup):
    main = soup.find('table', {"class": "all"})
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
    return div_big_panel_content



