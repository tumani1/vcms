#coding: utf-8
import json
import os
import argparse
from bs4 import BeautifulSoup
import datetime
from multi_key_dict import multi_key_dict
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from models import Media, Users, Persons, PersonsMedia, Topics, MediaUnits, MediaInUnit, CDN, Extras, MediaLocations
from models.extras.constants import APP_EXTRA_TYPE_VIEDO, APP_EXTRA_TYPE_IMAGE
from models.media.constants import APP_MEDIA_TYPE_VIDEO
from models.topics.constants import TOPIC_STATUS
from models.users.constants import APP_USERS_TYPE_GENDER, APP_USERS_GENDER_MAN
from utils.connection import get_session, mongo_connect
from utils.robots.support_functions import get_valid_date_for_str, implement_media_structure_fizruk

session = get_session()
mongodb_session = mongo_connect()




def datadir_fileiterator(datadir):
    for subdir in os.listdir(datadir):
        subdir_full = os.path.abspath(
                    os.path.join(datadir,
                                 subdir))
        
        filepath = next(jsonfile for jsonfile in os.listdir(subdir_full) if jsonfile.endswith('.json'))

        full_filepath = os.path.join(subdir_full,filepath)
        if os.path.exists(full_filepath):
            yield full_filepath


def parse_one_info_page(filepath):
    page_info = {
        'label': '',
        'value': '',
        'id':'',
        'description': '',
        'date': None,
        'actors': []
    }
    with open(filepath) as  opened_page:
        try:
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
        except :

            import traceback
            traceback.print_exc()


def parse_for_dir(jsons_dir = None):
    files = os.listdir(jsons_dir)
    fl = []
    for f in files:
        f = jsons_dir + f
        fl = fl + [f]
    parse_all_series(fl)


def parse_all_series(filenames_iterator):
    cdn = get_or_create_cdn("Своя CDN", "http://cdn.serialov.tv/")
    topic = get_or_create_topic("fizruk", "Физрук")
    for file_name in filenames_iterator:
        print file_name.split('/')[len(file_name.split('/'))-1].split('_')[1]
        m_unit = get_or_create_media_unit('Сезон {}'.format(file_name.split('/')[len(file_name.split('/'))-1].split('_')[1]), topic.name)
        one_info = parse_one_info_page(file_name)
        fake_user = get_or_create_user("Физрук", "Админ", APP_USERS_GENDER_MAN, 'password')
        media = get_or_create_media(one_info['label'], one_info['description'], one_info['date'], APP_MEDIA_TYPE_VIDEO, fake_user.id)
        get_or_create_media_in_unit(media.id, m_unit.id)
        get_or_create_extras(cdn, cdn.url+'content/media/{id}/poster.jpg', one_info['label'], ' ', one_info['description'], type=APP_EXTRA_TYPE_IMAGE)
        #get_or_create_extras(cdn, cdn.url+'v/{id}/hd.mp4', one_info['label'], ' ', one_info['description'])
        get_or_create_media_location(cdn.name, media.id, cdn.url+'v/{id}/hd.mp4'.format(id=media.id))
        implement_media_structure_fizruk(media, '/cdn/downloads/next_tv/static/upload/Fizruk/')   #'~/next_tv/static/upload/Fizruk/'
        for pers in one_info['actors']:
            name_surname = pers.split(' ')
            name = name_surname[0]
            surname = name_surname[1]
            person = get_or_create_person(name, surname)
            get_or_create_persons_media(media.id, person.id)

        print json.dumps({'id':media.id, 'filename': os.path.basename(file_name)})
        #print media.title, media.description, media.release_date, media.type_


    
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


def get_or_create_cdn(name, url):
    cdn = None
    try:
        cdn = session.query(CDN).filter(CDN.name == name).filter(CDN.url == url).one()
    except NoResultFound:
        cdn = CDN(name=name, url=url)
        session.add(cdn)
        session.commit()
    except Exception, e:
        print "EEE cdn" + e.message
        session.rollback()
        session.flush()
    return cdn


def get_or_create_extras(cdn, url, title, title_orig='', description='', type = APP_EXTRA_TYPE_VIEDO):
    extras = None
    try:
        extras = session.query(Extras).filter(Extras.cdn_name == cdn.name).filter(Extras.title == title).filter(Extras.type == type).one()
    except NoResultFound:
        extras = Extras(cdn_name=cdn.name, location='', title=title, title_orig= title_orig, description=description, type=type)
        session.add(extras)
        session.commit()

    except MultipleResultsFound:
        session.query(Extras).filter(Extras.cdn_name == cdn.name).filter(Extras.title == title).filter(Extras.type == type).delete(False)
        session.commit()
        extras = Extras(cdn_name=cdn.name, location='', title=title, title_orig= title_orig, description=description, type=type)
        session.add(extras)
        session.commit()
    except Exception, e:
        print "EEE ex" + e.message
        session.rollback()
        session.flush()

    extras.location = url.format(id=extras.id)
    session.commit()
    print "URL:", extras.location
    return extras


def get_or_create_media_in_unit(media_id, media_unit_id):
    media_in_unit = None
    try:
        media_in_unit = session.query(MediaInUnit).filter(MediaInUnit.media_unit_id == media_unit_id).filter(MediaInUnit.media_id == media_id).one()
    except NoResultFound:
        media_in_unit = MediaInUnit(media_id=media_id, media_unit_id=media_unit_id)
        session.add(media_in_unit)
        session.commit()
    except Exception, e:
        print "EEE" + e.message
        session.rollback()
        session.flush()
    return media_in_unit


def get_or_create_topic(name, title, releasedate = datetime.datetime.today().date()):
    topic = None
    try:
        topic = session.query(Topics).filter(Topics.name == name).one()
        print "after"
    except NoResultFound:
        topic = Topics(name=name, title=title, releasedate=releasedate, status=u'a', type=u'serial')
        session.add(topic)
        session.commit()
    except Exception, e:
        print "EEE t " + e.message
        session.rollback()
        session.flush()
    return topic


def get_or_create_media_unit(title, topic_id):
    m_unit = None
    try:
        m_unit = session.query(MediaUnits).filter(MediaUnits.title == title).filter(MediaUnits.topic_id == topic_id).one()
    except NoResultFound:
        m_unit = MediaUnits(title=title, topic_id=topic_id)
        session.add(m_unit)
        session.commit()
    except Exception, e:
        print "EEE" + e.message
        session.rollback()
        session.flush()
    return m_unit



def get_or_create_user(fname, lname, gender, password):
    user = None
    try:
        user = session.query(Users).filter(Users.firstname == fname).filter(Users.lastname == lname).one()
    except NoResultFound:
        user = Users(firstname=fname, lastname=lname, gender=APP_USERS_GENDER_MAN, password=password)
        session.add(user)
        session.commit()
    except Exception, e:
        print "fuser err" + e.message
        session.rollback()
        session.flush()
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
        session.rollback()
        session.flush()
    return pers_media


def get_or_create_media(title, description, release_date, type_, owner):
    media = None
    try:
        owner_sa  = session.query(Users).filter(Users.id == owner).one()
        media = session.query(Media).filter(Media.title == title).one()
    except NoResultFound:
        try:
            media = Media(title=title, description=description, release_date=release_date, type_=type_, owner=owner_sa)
        except Exception, e:
            print "EEE" + e.message
            import traceback
            traceback.print_exc()
        session.add(media)
        session.commit()
    except Exception, e:
        print "EEE" + e.message
        session.rollback()
        session.flush()
    return media


def get_or_create_media_location(cdn_name, media_id, url=''):
    media_location = None
    try:
        media_location = session.query(MediaLocations).filter(MediaLocations.media_id == media_id, MediaLocations.cdn_name == cdn_name).one()
        media_location.location = url
        session.commit()
    except NoResultFound:
        media_location = MediaLocations(media_id=media_id, cdn_name=cdn_name, value=url)
        session.add(media_location)
        session.commit()
    except MultipleResultsFound:
        session.query(MediaLocations).filter(MediaLocations.media_id == media_id, MediaLocations.cdn_name == cdn_name).delete(False)
        session.commit()
        media_location = MediaLocations(media_id=media_id, cdn_name=cdn_name, value=url)
        session.add(media_location)
        session.commit()
    except Exception, e:
        session.rollback()
        session.flush()
    return media_location

if __name__ =="__main__":

    # files = os.listdir('saved_pages/fizruk/')
    #
    # import subprocess
    # for f in files:
    #     os.makedirs(f.split('.')[0].split('_')[3])
    #     os.system("mv {1} {0}/".format(f.split('.')[0].split('_')[3],'saved_pages/fizruk/'+f))

    parser = argparse.ArgumentParser("Import utility.")
    parser.add_argument('datadir', type=str, help = 'Directory containing subdirs, every subdir expected to contain json and mp4 file with same name')
    args = parser.parse_args()
    parse_all_series(datadir_fileiterator(args.datadir))
    
