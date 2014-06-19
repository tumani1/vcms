import datetime
from models import db, MediaUnits, UsersMediaUnits


@db
def create_media_units(session=None):
    mu1 = MediaUnits(topic_name='test11', title='mu1', title_orig=1, description='test1', next_unit=2, release_date=datetime.datetime(2011,1,1,0,0,0), end_date=datetime.datetime(2014,2,1,0,0,0), batch='batch1')
    mu2 = MediaUnits(topic_name='test11', title='mu2', title_orig=2, description='test2', previous_unit=1, next_unit=3, release_date=datetime.datetime(2012,1,1,0,0,0), end_date=datetime.datetime(2014,2,1,0,0,0), batch='batch1')
    mu3 = MediaUnits(topic_name='test11', title='mu3', title_orig=3, description='test3', previous_unit=2, release_date=datetime.datetime(2013,1,1,0,0,0), end_date=datetime.datetime(2014,2,1,0,0,0), batch='batch1')
    user_mu1 = UsersMediaUnits(media_unit_id=1, user_id=1, watched=datetime.datetime(2014,1,1,0,0,0))
    user_mu2 = UsersMediaUnits(media_unit_id=2, user_id=1, watched=datetime.datetime(2014,1,1,0,0,0))
    session.add_all([mu1, mu2, mu3, user_mu1, user_mu2])
    session.commit()