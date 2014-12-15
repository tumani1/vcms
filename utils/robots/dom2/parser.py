# coding: utf-8
import json
import locale
from bs4 import BeautifulSoup
from models.media.constants import APP_MEDIA_TYPE_VIDEO
from models.users.constants import APP_USERS_GENDER_MAN
from utils.robots.dom2.loader import load_pages, load_video_info_page, load_old_actors_pages, load_current_actors_page
from utils.robots.dom2.parser_supp import get_episods_for_page, get_b_big_panel_content_div
from utils.robots.fizruk.parser import get_or_create_user, get_or_create_media, get_or_create_person, \
    get_or_create_persons_media, get_or_create_cdn, get_or_create_topic, get_or_create_media_unit, \
    get_or_create_media_in_unit, get_or_create_extras, get_or_create_media_location
from utils.robots.support_functions import get_valid_date_for_str, save_poster_to_file, format_dom_2_name_str

__author__ = 'vladimir'

#episode = один день

def parse_all_pages():
    all_episods_info = []
    locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
    pages = []
    pages = load_pages()
    all_actors = get_all_actors()
    for page in pages:
        all_episods_info = all_episods_info + parse_one_page(page, all_actors)
    return all_episods_info


def parse_one_page(page, all_actors):
    episods_informations = []
    opned_page = open(page)
    json_page = json.load(opned_page)
    beatiful_soup = BeautifulSoup(json_page['html'])
    episods = get_episods_for_page(beatiful_soup)

    for episode in episods:
        try:
            episod_quick_info = get_episode_quick_info(episode)
            episods_informations = episods_informations + [parse_one_episode(episod_quick_info, all_actors)]

        except Exception, e:
            import traceback
            traceback.print_exc()
            continue
    return episods_informations


def parse_one_episode(episod_quick_info, all_actors):
    video_info_page = load_video_info_page(episod_quick_info['video_info_page_url'], episod_quick_info['label'])
    if not video_info_page:
        print "No video details page loaded!"
        return
    opned_page = open(video_info_page)
    json_page = json.load(opned_page)
    beatiful_soup = BeautifulSoup(json_page['html'])
    episod_info = parse_video_page(beatiful_soup)
    episod_info['actors'] = get_actors_for_episode(episod_info['date'], all_actors)

    cdn = get_or_create_cdn("Своя CDN", "http://cdn.serialov.tv/")
    topic = get_or_create_topic("dom2", "Дом 2")
    m_unit = get_or_create_media_unit('Все серии',topic.name)
    fake_user = get_or_create_user("Дом2", "Админ", APP_USERS_GENDER_MAN, 'password')
    if u"день" in episod_info['label']:
        media = get_or_create_media(format_dom_2_name_str(episod_info['label']), episod_info['description'], episod_info['date'], APP_MEDIA_TYPE_VIDEO, fake_user.id)
        get_or_create_media_in_unit(media.id, m_unit.id)
        get_or_create_extras(cdn.name, cdn.url+'s/upload/media/{id}/poster.jpg'.format(id=media.id), episod_info['label'], ' ', episod_info['description'])
        get_or_create_media_location(cdn.name, media.id, cdn.url)
    for pers in episod_info['actors']:
        name_surname = pers['name'].split(' ')
        name = name_surname[0]
        surname = name_surname[1]
        if u"день" in episod_info['label']:
            person = get_or_create_person(name, surname)
            get_or_create_persons_media(media.id, person.id)
    print "Parsed ", episod_quick_info['label']
    return episod_info


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
        quick_info['poster'] = save_poster_to_file(poster_link, format_dom_2_name_str(quick_info['label']))
    return quick_info


def parse_video_page(soup):

    episode_info = {
        'label': '',
        'date': None,
        'description': '',
        'value': '',
        'actors': []
    }
    div_big_panel_content = get_b_big_panel_content_div(soup)
    photo_panel_table = div_big_panel_content.find('table', {"class": "photo-panel all-height"})

    episode_info['date'] = get_video_date(photo_panel_table)
    episode_info['label'] = get_video_label(photo_panel_table)
    print episode_info['label']
    episode_info['description'] = get_video_description(photo_panel_table)
    episode_info['value'] = get_video_embedded_code(photo_panel_table)
    return episode_info



def get_actors_for_episode(episode_date, all_actors):
    episode_actors = []
    for actor in all_actors:
        if is_actor_played(actor, episode_date):
            episode_actors = episode_actors + [actor]
    return episode_actors


def is_actor_played(actor, date):
    if date is None:
        return False
    if (actor['finish_date'] is None) and (actor['start_date'] <= date):
        return True
    if not (actor['finish_date'] is None) and (actor['finish_date'] >= date) and (actor['start_date'] <= date):
        return True
    return False


def get_all_actors():
    old = get_old_actors()
    current = get_current_actors()
    all_actors = old + current
    return all_actors


def get_old_actors():
    actors = []
    pages = load_old_actors_pages()
    for page in pages:
        try:
            actors = actors + parse_one_actors_page(page)
        except Exception, e:
            continue
    return actors

def parse_one_actors_page(page):
    old_actors_from_one_page = []
    opned_page = open(page)
    json_page = json.load(opned_page)
    beatiful_soup = BeautifulSoup(json_page['html'])
    actors_descrs = beatiful_soup.findAll('td', {"class": "descr"})
    for actor in actors_descrs:
        actor_inf = get_one_actor_info(actor)
        old_actors_from_one_page = old_actors_from_one_page + [actor_inf]
    return old_actors_from_one_page


def get_current_actors():
    current_actors = []
    actorspage = load_current_actors_page()
    opned_page = open(actorspage)
    json_page = json.load(opned_page)
    beatiful_soup = BeautifulSoup(json_page['html'])
    actors_descrs = beatiful_soup.findAll('td', {"class": "descr"})
    for actor in actors_descrs:
        actor_inf = get_one_actor_info(actor)
        current_actors = current_actors + [actor_inf]
    return current_actors


def get_one_actor_info(actor_div):

    actor_info = {
        'name': '',
        'start_date': None,
        'finish_date': None,
        'profile_link': ''
    }

    nik = actor_div.find('a', {"class": "nik"})
    name = nik.text
    profile_link = nik['href']
    div = actor_div.find('div', {"class": "txt"})
    nobrs = div.findAll('nobr')
    actor_info['start_date'] = get_valid_date_for_str(nobrs[0].text)
    if len(nobrs) > 1:
        actor_info['finish_date'] = get_valid_date_for_str(nobrs[1].text)

    actor_info['name'] = name
    actor_info['profile_link'] = 'http://dom2.ru' + profile_link

    return actor_info


def get_video_date(photo_panel_class):
    botton_line_td = photo_panel_class.find('td', {"class": "bottom-line"})
    div_calendar = botton_line_td.find('div', {"class": "calendar-td"})
    div_green_box = div_calendar.find('div', {"class": "greenBox"})
    span_green_box_date = div_green_box.find('span', {"class": "greenBoxDate"})
    a_link = span_green_box_date.find('a', {"class": "link no-select"})
    e_date = get_valid_date_for_str(a_link.find('nobr').text)
    return e_date


def get_video_description(photo_panel_class):
    try:
        div_content_text = photo_panel_class.find('div', {"class": "content-text"})
        p_tag = div_content_text.find('p')
        description = p_tag.text
    except Exception, e:
        description = ''
    return description


def get_video_embedded_code(photo_panel_class):
    #div_movie_container = photo_panel_class.findAll('div', {"id": "movieContainer"})
    #if not div_movie_container:
    #    return ''
    #code = div_movie_container.find('embed', {"id": "player"})
    #print "code", code
    return ''#code


def get_video_label(photo_panel_class):
    h2 = photo_panel_class.find('h2')
    label = h2.text
    return label
