# coding: utf-8
import datetime
from models import Topics, UsersTopics, Users, CDN, Extras, ExtrasTopics, MediaUnits, UsersMediaUnits, Countries, Cities, Scheme, UsersValues, \
    UsersMsgrThreads, MsgrThreads, MsgrLog
from models.users import UsersRels
from models.users.constants import APP_USERSRELS_TYPE_FRIEND


def create_media_units(session):
    mu1 = MediaUnits(topic_name='test1', title='mu1', title_orig=1, description='test1', next_unit=2, release_date=datetime.datetime(2011,1,1,0,0,0), end_date=datetime.datetime(2014,2,1,0,0,0), batch='batch1')
    mu2 = MediaUnits(topic_name='test1', title='mu2', title_orig=2, description='test2', previous_unit=1, next_unit=3, release_date=datetime.datetime(2012,1,1,0,0,0), end_date=datetime.datetime(2014,2,1,0,0,0), batch='batch1')
    mu3 = MediaUnits(topic_name='test1', title='mu3', title_orig=3, description='test3', previous_unit=2, release_date=datetime.datetime(2013,1,1,0,0,0), end_date=datetime.datetime(2014,2,1,0,0,0), batch='batch1')
    user_mu1 = UsersMediaUnits(media_unit_id=1, user_id=1, watched=datetime.datetime(2014,1,1,0,0,0))
    user_mu2 = UsersMediaUnits(media_unit_id=2, user_id=1, watched=datetime.datetime(2014,1,1,0,0,0))
    session.add_all([mu1, mu2, mu3, user_mu1, user_mu2])
    session.commit()


def create_topic(session):
    list_topics = [
        Topics(name="test", title="test", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0,0), status="a", type="news"),
        Topics(name="test1", title="test1", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0,0), status="a", type="news"),
        Topics(name="test2", title="test2", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0,0), status="a", type="show"),
    ]

    session.add_all(list_topics)
    session.commit()


def create_user_topic(session):
    list_uts = [
        UsersTopics(user_id=1, topic_name="test"),
        UsersTopics(user_id=1, topic_name="test1", subscribed=datetime.datetime(2014,1,1,0,0,0,0)),
        UsersTopics(user_id=1, topic_name="test2", liked=datetime.datetime(2014,1,1,0,0,0,0)),
    ]

    session.add_all(list_uts)
    session.commit()


def create_cdn(session):
    list_cdn = [
        CDN(name="cdn1", description="test", has_mobile=False, has_auth=False, url="ya.ru", location_regxp="", cdn_type=""),
        CDN(name="cdn2", description="test", has_mobile=False, has_auth=True, url="google.com", location_regxp="", cdn_type=""),
    ]

    session.add_all(list_cdn)
    session.commit()


def create_extras(session):
    list_extras = [
        Extras(cdn_name='cdn1', type="v", location="russia", description="test test", title="test", title_orig="test", created=datetime.datetime(2014,1,1,0,0,0,0)),
        Extras(cdn_name='cdn1', type="v", location="russia", description="test1 test", title="test1", title_orig="test1", created=datetime.datetime(2014,1,1,0,0,0,0)),
        Extras(cdn_name='cdn1', type="a", location="russia", description="test2 test", title="test2", title_orig="test2", created=datetime.datetime(2014,1,1,0,0,0,0)),
        Extras(cdn_name='cdn1', type="a", location="russia", description="test test", title="test", title_orig="test", created=datetime.datetime(2014,1,1,0,0,0,0)),
        Extras(cdn_name='cdn2', type="v", location="russia", description="test1 test", title="test1", title_orig="test1", created=datetime.datetime(2014,1,1,0,0,0,0)),
        Extras(cdn_name='cdn2', type="v", location="russia", description="test2 test", title="test2", title_orig="test2", created=datetime.datetime(2014,1,1,0,0,0,0)),
    ]

    session.add_all(list_extras)
    session.commit()


def create_topic_extras(session):
    list_te = [
        ExtrasTopics(extras_id=1, topic_name="test"),
        ExtrasTopics(extras_id=1, topic_name="test1"),
        ExtrasTopics(extras_id=1, topic_name="test2"),
        ExtrasTopics(extras_id=2, topic_name="test"),
        ExtrasTopics(extras_id=3, topic_name="test1"),
        ExtrasTopics(extras_id=4, topic_name="test2"),
    ]


    session.add_all(list_te)
    session.commit()


def create(session):
    country = Countries(name='Test', name_orig="Test")
    session.add(country)
    session.commit()

    city = Cities(country=country, name="Test", name_orig="Test", time_zone='UTC')
    session.add(city)
    session.commit()

    user = Users(city=city, firstname="Test1", lastname="Test1", password='Test1', email='test1@test.ru')
    session.add(user)
    session.commit()
    user2 = Users(city=city, firstname="Test2", lastname="Test2", password='Test2', email='test2@test.ru')
    user3 = Users(city=city, firstname="Test3", lastname="Test3", password='Test3', email='test3@test.ru')
    session.add_all([user2, user3])
    session.commit()

    return user.id


def create_scheme(session):
    shm1 = Scheme(topic_name='test1', name='shm1', internal=False)
    shm2 = Scheme(topic_name='test1', name='shm2', internal=False)
    session.add_all([shm1, shm2])
    session.commit()


def create_users_values(session):
    user_val1 = UsersValues(scheme_id=1, user_id=1, value_int=777)
    session.add(user_val1)
    session.commit()


def create_users_rels(session):
    user_rels1 = UsersRels(user_id=1, partner_id=2, urStatus=APP_USERSRELS_TYPE_FRIEND)
    user_rels2 = UsersRels(user_id=2, partner_id=3, urStatus=APP_USERSRELS_TYPE_FRIEND)
    user_rels3 = UsersRels(user_id=2, partner_id=1, urStatus=APP_USERSRELS_TYPE_FRIEND)
    user_rels4 = UsersRels(user_id=3, partner_id=2, urStatus=APP_USERSRELS_TYPE_FRIEND)
    session.add_all([user_rels1, user_rels2, user_rels3, user_rels4])
    session.commit()


def create_users_msgr_threads(session):
    users_msgr_threads1 = UsersMsgrThreads(user_id=1, msgr_threads_id=1, last_msg_sent=datetime.datetime(2014,1,1,0,0,0,0), last_visit=datetime.datetime(2014,1,1,0,0,0,0), new_msgs=1)
    users_msgr_threads2 = UsersMsgrThreads(user_id=2, msgr_threads_id=1, last_msg_sent=datetime.datetime(2014,1,1,0,0,0,0), last_visit=datetime.datetime(2014,1,1,0,0,0,0), new_msgs=1)
    session.add_all([users_msgr_threads1, users_msgr_threads2])
    session.commit()


def create_msgr_threads(session):
    msgr_threads = MsgrThreads(msg_cnt=2)
    session.add(msgr_threads)
    session.commit()


def create_msgr_log(session):
    msgr_log = MsgrLog(msgr_threads_id=1, user_id=1, created=datetime.datetime(2014,1,1,0,0,0,0), text='text')
    session.add(msgr_log)
    session.commit()