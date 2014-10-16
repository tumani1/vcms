# coding: utf-8
import datetime
import pytz
from models import *
from models.users.constants import APP_USERSRELS_TYPE_FRIEND, APP_USERSRELS_BLOCK_TYPE_MATUALLY

UTC = pytz.utc


def create_media_units(session):
    mu1 = MediaUnits(topic_name='test1', title='mu1', title_orig=1, description='test1', next_unit=2, release_date=datetime.datetime(2011,1,1,0,0,0,tzinfo=UTC), end_date=datetime.datetime(2014,2,1,0,0,0, tzinfo=UTC), batch='batch1')
    mu2 = MediaUnits(topic_name='test1', title='mu2', title_orig=2, description='test2', previous_unit=1, next_unit=3, release_date=datetime.datetime(2012,1,1,0,0,0, tzinfo=UTC), end_date=datetime.datetime(2014,2,1,0,0,0, tzinfo=UTC), batch='batch1')
    mu3 = MediaUnits(topic_name='test1', title='mu3', title_orig=3, description='test3', previous_unit=2, release_date=datetime.datetime(2013,1,1,0,0,0, tzinfo=UTC), end_date=datetime.datetime(2014,2,1,0,0,0, tzinfo=UTC), batch='batch1')
    user_mu1 = UsersMediaUnits(media_unit_id=1, user_id=1, watched=datetime.datetime(2014,1,1,0,0,0, tzinfo=UTC))
    user_mu2 = UsersMediaUnits(media_unit_id=2, user_id=1, watched=datetime.datetime(2014,1,1,0,0,0, tzinfo=UTC))

    session.add_all([mu1, mu2, mu3, user_mu1, user_mu2])
    session.commit()


def create_media(session):
    media1 = Media(title='media1', type_='v', owner=1, title_orig='test_media1', description='test_desc1', created=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC))
    media2 = Media(title='media2', type_='v', owner=1, title_orig='test_media2', description='test_desc2', created=datetime.datetime(2014,2,1,0,0,0,0, tzinfo=UTC))
    media3 = Media(title='media3', type_='v', owner=1, title_orig='test_media3', description='test_desc3', created=datetime.datetime(2014,2,1,0,0,0,0, tzinfo=UTC))
    media4 = Media(title='media4', type_='v', owner=1, title_orig='test_media4', description='test_desc4', created=datetime.datetime(2014,2,1,0,0,0,0, tzinfo=UTC))

    m_in_u1 = MediaInUnit(media_id=1, media_unit_id=2)
    m_in_u2 = MediaInUnit(media_id=2, media_unit_id=1)

    user_m1 = UsersMedia(media_id=1, user_id=1, views_cnt=5, play_pos=50, playlist=datetime.datetime(2013,2,1,0,0,0,0, tzinfo=UTC), liked=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC), watched=datetime.datetime(2013,1,1,0,0,0,0, tzinfo=UTC))
    user_m2 = UsersMedia(media_id=2, user_id=1, views_cnt=10, watched=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC))
    user_m3 = UsersMedia(media_id=3, user_id=1, views_cnt=10, play_pos=20, playlist=datetime.datetime(2014,2,1,0,0,0,0, tzinfo=UTC), watched=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC))
    user_m4 = UsersMedia(media_id=4, user_id=1, views_cnt=5, play_pos=50, playlist=datetime.datetime(2013,2,1,0,0,0,0, tzinfo=UTC), liked =datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC), watched=datetime.datetime(2013,1,1,0,0,0,0, tzinfo=UTC))
    pers_m1 = PersonsMedia(media_id=1, person_id=1, role='actor')

    session.add_all([media1, media2, media3,media4, m_in_u1, m_in_u2, user_m1, user_m2, user_m3, user_m4, pers_m1])
    session.commit()

def create_persons(session):
    persons = [
        Persons(user_id=1, firstname='test', lastname='testov', bio='test_bio'),
        Persons(user_id=2, firstname='test2', lastname='testov2', bio='test_bio'),
        Persons(firstname='test3', lastname='testov3', bio='test_bio'),
        Persons(user_id=3, firstname='test4', lastname='testov4', bio='test_bio'),
        Persons(firstname='test5', lastname='testov5', bio='test_bio'),
    ]

    session.add_all(persons)
    session.commit()

def create_comments(session):
    com1 = Comments(user_id=1, text=u'Тест', created=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC), obj_type='m', obj_id=1)
    com2 = Comments(user_id=1, text=u'Тест2', created=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC), obj_type='mu', obj_id=1)
    com3 = Comments(user_id=1, text=u'Тест3', created=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC), obj_type='mu', obj_id=1)
    user_com1 = UsersComments(user_id=1, comment_id=3, liked=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC))

    session.add_all([com1, com2, com3, user_com1])
    session.commit()

def create_topic(session):
    list_topics = [
        Topics(name="test", title="test", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC), status="a", type="news"),
        Topics(name="test1", title="test1", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC), status="a", type="news"),
        Topics(name="test2", title="test2", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC), status="a", type="show"),
    ]

    session.add_all(list_topics)
    session.commit()


def create_user_topic(session):
    list_uts = [
        UsersTopics(user_id=1, topic_name="test"),
        UsersTopics(user_id=1, topic_name="test1", subscribed=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC)),
        UsersTopics(user_id=1, topic_name="test2", liked=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC)),
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


def create_one_media(session):
    user = Users(firstname="Test", lastname="Test", password='Test', email='test@test.ru')
    session.add(user)
    session.commit()
    media = Media(title='Test', type_='v', owner=user.id, title_orig='test_media1', description='test_desc1')
    session.add(media)
    session.commit()


def create_persons_media(session):
    user = Users(firstname="User", lastname="User", password='Test', email='user@test.ru')
    media = Media(title='Test', type_='v', user_owner=user, title_orig='test_media1', description='test_desc1')
    person = Persons(users=user, firstname='test', lastname='test', bio='test_bio')
    person_media = PersonsMedia(media=media, persons=person, role='actor')
    session.add_all([media, user, person, person_media])
    session.commit()


def create_extras(session):
    list_extras = [
        Extras(cdn_name='cdn1', type="v", location="russia", description="test test", title="test", title_orig="test", created=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC)),
        Extras(cdn_name='cdn1', type="v", location="russia", description="test1 test", title="test1", title_orig="test1", created=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC)),
        Extras(cdn_name='cdn1', type="a", location="russia", description="test2 test", title="test2", title_orig="test2", created=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC)),
        Extras(cdn_name='cdn1', type="a", location="russia", description="test test", title="test", title_orig="test", created=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC)),
        Extras(cdn_name='cdn2', type="v", location="russia", description="test1 test", title="test1", title_orig="test1", created=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC)),
        Extras(cdn_name='cdn2', type="v", location="russia", description="test2 test", title="test2", title_orig="test2", created=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC)),
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

def create_person_extras(session):
    list_pe = [
        PersonsExtras(extras_id=1, person_id=1),
        PersonsExtras(extras_id=1, person_id=2),
        PersonsExtras(extras_id=1, person_id=3),
        PersonsExtras(extras_id=2, person_id=1),
        PersonsExtras(extras_id=3, person_id=2),
        PersonsExtras(extras_id=4, person_id=3),
    ]

    session.add_all(list_pe)
    session.commit()


def create(session):
    country = session.query(Countries).get('RU')

    city = Cities(country=country, region="76", name="Test", name_orig="Test", time_zone='UTC')
    session.add(city)
    session.commit()

    user = Users(city=city, firstname="Test1", lastname="Test1", password='Test1', email='test1@test.ru', created=datetime.datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=UTC))
    session.add(user)
    session.commit()

    user2 = Users(city=city, firstname="Test2", lastname="Test2", password='Test2', email='test2@test.ru', created=datetime.datetime(2012, 2, 1, 0, 0, 0, 0, tzinfo=UTC))
    user3 = Users(city=city, firstname="Test3", lastname="Test3", password='Test3', email='test3@test.ru', created=datetime.datetime(2012, 3, 1, 0, 0, 0, 0, tzinfo=UTC))
    session.add_all([user2, user3])
    session.commit()

    return user.id


def create_scheme(session):
    shms = [
        Scheme(topic_name='test1', name='shm1', internal=False),
        Scheme(topic_name='test1', name='shm2', internal=False)
    ]

    session.add_all(shms)
    session.commit()


def create_users_values(session):
    user_val1 = UsersValues(scheme_id=1, user_id=1, value_int=777)

    session.add(user_val1)
    session.commit()


def create_users_rels(session):
    user_rels = [
        UsersRels(user_id=1, partner_id=2, urStatus=APP_USERSRELS_TYPE_FRIEND),
        UsersRels(user_id=2, partner_id=3, urStatus=APP_USERSRELS_TYPE_FRIEND),
        UsersRels(user_id=2, partner_id=1, urStatus=APP_USERSRELS_TYPE_FRIEND),
        UsersRels(user_id=3, partner_id=2, urStatus=APP_USERSRELS_TYPE_FRIEND),
        UsersRels(user_id=1, partner_id=3, blocked=APP_USERSRELS_BLOCK_TYPE_MATUALLY),
        UsersRels(user_id=3, partner_id=1, blocked=APP_USERSRELS_BLOCK_TYPE_MATUALLY),
    ]
    session.add_all(user_rels)
    session.commit()


def create_users_msgr_threads(session):
    users_msgr = [
        UsersMsgrThreads(user_id=1, msgr_threads_id=1, last_msg_sent=datetime.datetime(2014,1,1,0,0,0,0,tzinfo=UTC), last_visit=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC), new_msgs=1),
        UsersMsgrThreads(user_id=2, msgr_threads_id=1, last_msg_sent=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC), last_visit=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC), new_msgs=1),
    ]

    session.add_all(users_msgr)
    session.commit()


def create_msgr_threads(session):
    msgr_threads = MsgrThreads(msg_cnt=2)

    session.add(msgr_threads)
    session.commit()


def create_msgr_log(session):
    msgr_log = MsgrLog(msgr_threads_id=1, user_id=1, created=datetime.datetime(2014,1,1,0,0,0,0, tzinfo=UTC), text='text')

    session.add(msgr_log)
    session.commit()


def create_persons_values(session):
    list_pev = [
        PersonsValues(scheme_id=1, person_id=1, value_int=777),
        PersonsValues(scheme_id=2, person_id=1, value_int=777),
        PersonsValues(scheme_id=1, person_id=2, value_int=777),
        PersonsValues(scheme_id=2, person_id=2, value_int=777),
        PersonsValues(scheme_id=1, person_id=2, value_string='test'),
        PersonsValues(scheme_id=1, person_id=2, value_text='test'),
    ]

    session.add_all(list_pev)
    session.commit()


def create_topic_values(session):
    list_tov = [
        TopicsValues(scheme_id=1, topic_name="test", value_int=777),
        TopicsValues(scheme_id=2, topic_name="test", value_int=777),
        TopicsValues(scheme_id=1, topic_name="test1", value_int=777),
        TopicsValues(scheme_id=2, topic_name="test1", value_int=777),
        TopicsValues(scheme_id=1, topic_name="test1", value_string='test'),
        TopicsValues(scheme_id=1, topic_name="test1", value_text='test'),
    ]

    session.add_all(list_tov)
    session.commit()


def create_content(session):
    content = Content(text='test', obj_id=1, obj_type='m')
    session.add(content)
    session.commit()


def create_chat(session):
    c = Chats(description='chat for testing')
    session.add(c)
    session.commit()


def create_users_chat(session):
    uc = UsersChat(user_id=1, chat_id=1, cuStatus='1')
    session.add(uc)
    session.commit()
<<<<<<< HEAD
=======


def create_categories(session):
    cat1 = Categories(name='category1', description='category_test')
    cat2 = Categories(name='category2', description='category2_test')
    cat3 = Categories(name='category3', description='category3_test')
    cat4 = Categories(name='category4', description='category4_test')
    session.add_all([cat1, cat2, cat3, cat4])
    session.commit()


def create_items_categories(session):
    item_cat = ItemsCategories(item_id=1, category_id=1)
    item_cat2 = ItemsCategories(item_id=2, category_id=2)
    item_cat3 = ItemsCategories(category_id=3)
    item_cat4 = ItemsCategories(category_id=4, item_id=3)
    item_cat5 = ItemsCategories(category_id=4, item_id=4)
    session.add_all([item_cat, item_cat2, item_cat3, item_cat4, item_cat5])
    session.commit()


def create_categories_extras(session):
    cat_extras = CategoriesExtras(categories_id=1, extras_id=1, extras_type=1)
    session.add(cat_extras)
    session.commit()


def create_items(session):
    item1 = Items(name='item1', description='item_test', active=True, instock=False)
    item2 = Items(name='item2', description='item2_test', active=True, instock=True)
    item3 = Items(name='item3', description='item3_test', active=True, instock=False)
    item4 = Items(name='item4', description='item4_test', active=True, instock=True)
    session.add_all([item1, item2, item3, item4])
    session.commit()


def create_items_extras(session):
    items_extras1 = ItemsExtras(item_id=1, extras_id=1)
    items_extras2 = ItemsExtras(item_id=2, extras_id=2)
    session.add_all([items_extras1, items_extras2])
    session.commit()


def create_variants(session):
    variants1 = Variants(item_id=1, name='variants1', description='variants1', price=1, price_old=1, active=True, stock_cnt=2, reserved_cnt=1 )
    variants2 = Variants(item_id=2, name='variants2', description='variants2', price=2, price_old=2, active=True)
    session.add_all([variants1, variants2])
    session.commit()


def create_variants_extras(session):
    variants_extras = VariantsExtras(variant_id=1, extras_id=2)
    session.add(variants_extras)
    session.commit()


def create_items_objects(session):
    items_objects = ItemsObjects(item_id=1, obj_name='obj1', obj_id=1, obj_type=u'c')
    session.add(items_objects)
    session.commit()


def create_cart(session):
    carts = Carts(user_id=1, items_cnt=1, cost_total=10, status='active', created='2014.02.02')
    session.add(carts)
    session.commit()


def create_items_carts(session):
    items_carts = ItemsCarts(carts_id=1, variant_id=1, cnt=1, price=10, cost=10)
    session.add(items_carts)
    session.commit()


def create_cart_log(session):
    cart_log = CartLog(cart_id=1, comment='cart')
    session.add(cart_log)
    session.commit()


def create_payments(session):
    payments = Payments(cart_id=1, status='active', cost=10, created='2014.02.02')
    session.add(payments)
    session.commit()



>>>>>>> origin/develop
