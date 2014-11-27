#coding: utf-8
import json
import os
from bs4 import BeautifulSoup
from multi_key_dict import multi_key_dict
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from models import Media, Users, Persons, PersonsMedia
from models.media.constants import APP_MEDIA_TYPE_VIDEO
from models.users.constants import APP_USERS_TYPE_GENDER, APP_USERS_GENDER_MAN
from utils.connection import get_session, mongo_connect
from utils.robots.support_functions import get_valid_date_for_str

__author__ = 'vladimir'

session = get_session()
mongodb_session = mongo_connect()



def parse_all_series(jsons_directory):
    files = os.listdir(jsons_directory)
    for file_name in files:
        one_info = parse_one_info_page(jsons_directory+file_name)
        fake_user = get_or_create_user("Физрук", "Админ", APP_USERS_GENDER_MAN, 'password')
        media = get_or_create_media(one_info['label'], one_info['description'], one_info['date'], APP_MEDIA_TYPE_VIDEO, fake_user.id)
        for pers in one_info['actors']:
            name_surname = pers.split(' ')
            name = name_surname[0]
            surname = name_surname[1]
            person = get_or_create_person(name, surname)
            pers_media = get_or_create_persons_media(media.id, person.id)
        #print media.title, media.description, media.release_date, media.type_


def parse_one_info_page(page):
    page_info = {
        'label': '',
        'value': '',
        'id':'',
        'description': '',
        'date': None,
        'actors': []
    }
    opened_page = open(page)
    json_page = json.load(opened_page)
    beatiful_soup = BeautifulSoup(json_page['html'])
    all = beatiful_soup.find('div', { "id" : "all"})
    content = all.find('div', { "id" : "content"})
    center_block = content.find('div', { "id" : "center-block"})
    date = get_date(center_block)
    decription = get_description(center_block)
    value = get_video_code(center_block)
    caption = get_caption(center_block)
    all_tags = get_actors_tags(center_block)
    actors_names = get_actors_names(all_tags)
    page_info['label'] = caption
    page_info['value'] = value
    page_info['description'] = decription
    page_info['date'] = date
    page_info['actors'] = actors_names
    return page_info


def get_video_code(center_block):
    video_player_now = center_block.find('div', { "id" : "video-player-now"})
    iframe = video_player_now.find('iframe')
    video_link = iframe['src']
    return video_link


def get_actors_tags(center_block):
    actors = []
    video_info = center_block.find('div', { "id" : "video-info"})
    steps = video_info.findAll('div', {"class": "step"})
    for step in steps:
        try:
            a_tags = step.findAll('a')
            for a_tag in a_tags:
                actors = actors + [a_tag.text]
        except Exception, e:
            continue
    return actors


def get_date(center_block):
    video_info = center_block.find('div', { "id" : "video-info"})
    left = video_info.find('div', { "class" : "left"})
    a = left.find('a')
    text_date = a.text
    return get_valid_date_for_str(text_date)


def get_description(center_block):
    video_info = center_block.find('div', { "id" : "video-info"})
    left = video_info.find('div', { "class" : "left"})
    v_descr = left.find('div', { "class" : "v_descr"})
    description = v_descr.text
    return description


def get_caption(center_block):
    h1 = center_block.find('h1')
    caption = h1.text
    return caption


def get_actors_names(tags):
    actors_names = []
    all_actors = get_all_actors()
    for tag in tags:
        try:
            act_name = all_actors[tag]
            if act_name not in actors_names:
                actors_names = actors_names + [act_name]
                print act_name
        except KeyError, e:
            continue
    return actors_names


def get_all_actors():
    all_actors = multi_key_dict()
    all_actors[u'Фомин', u'Олег Евгеньевич', u'Дмитрий Нагиев', u'Физрук', u'Фома'] = u'Дмитрий Нагиев'
    all_actors[u'Александра Мамаева', u'Мамаева', u'Саша Мамаева'] = u'Полина Грец'
    all_actors[u'Валентин Вялых', u'Усач'] = u'Даниил Вахрушев'
    all_actors[u'Антон Борисов', u'Борзый'] = u'Артур Сопельник'
    all_actors[u'Александр Бодягин', u'Банан'] = u'Андрей Крыжний'
    all_actors[u'Алена Лазукова', u'Пупок'] = u'Виктория Клинкова'
    all_actors[u'Татьяна Александровна', u'Анастасия Панина'] = u'Анастасия Панина'
    all_actors[u'Светлана Петровна', u'Светик'] = u'Карина Мишулина'
    all_actors[u'Лев Романович'] = u'Евгение Кулаков'
    all_actors[u'Эльвира Петровна', u'Завуч'] = u'Елена Муравьева'
    all_actors[u'Слава', u'Славян'] = u'Владимир Жеребцов'
    all_actors[u'Виктор Николаевич', u'Мамай', u'Александр Гордон'] = u'Александр Гордон'
    all_actors[u'Алексей Алексеич', u'Лёха', u'Псих'] = u'Владимир Сычев'
    all_actors[u'Полина'] = u'Оксана Сидоренко'
    return all_actors


def get_or_create_user(fname, lname, gender, password):
    user = None
    try:
        user = session.query(Users).filter(Users.firstname == fname).filter(Users.lastname == lname).one()
    except NoResultFound:
        user = Users(firstname=fname, lastname=lname, gender=gender, password=password)
        session.add(user)
        session.commit()
    except Exception, e:
        print "User:", e.message
        session.rollback()
        session.flush()
    print user.id
    return user


def get_or_create_person(name, surname):
    person = None
    try:
        person = session.query(Persons).filter(Persons.firstname == name).filter(Persons.lastname == surname).one()
    except NoResultFound:
        person = Persons(firstname=name, lastname=surname)
        session.add(person)
        session.commit()
    except Exception, e:
        import traceback
        traceback.print_exc()
        print "Person:", e.message
        session.rollback()
        session.flush()
    return person


def get_or_create_persons_media(media_id, person_id):
    pers_media = None
    try:
        pers_media = session.query(PersonsMedia).filter(PersonsMedia.media_id == media_id, PersonsMedia.person_id == person_id).one()
    except NoResultFound:
        pers_media = PersonsMedia(media_id=media_id, person_id=person_id)
        session.add(pers_media)
        session.commit()
    except Exception, e:
        print "Pers_Media:", e.message
        session.rollback()
        session.flush()
    return pers_media


def get_or_create_media(title, description, release_date, type_, owner):
    media = None
    try:
        media = session.query(Media).filter(Media.title == title, Media.description == description,
                              Media.release_date == release_date, Media.type_ == type_, Media.owner == owner).one()
    except NoResultFound:
        media = Media(title=title, description=description, release_date=release_date, type_=type_, owner=owner)
        session.add(media)
        session.commit()
    except Exception, e:
        print "Media:", e.message
        session.rollback()
        session.flush()
    return media
