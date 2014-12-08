# coding: utf-8
import datetime

from mongoengine import Q

from models.mongo import Stream
from models.persons import UsersPersons
from utils import need_authorization


@need_authorization
def get(auth_user, session, **kwargs):
    person_ids = [_id[0] for _id in session.query(UsersPersons.person_id).filter(UsersPersons.user_id == auth_user.id).all()]
    stream_object_count = Stream.objects(Q(__raw__={'created': {"$gte": auth_user.checked_stream}}), Q(user_id=auth_user.id) | Q(__raw__={'attachments.id': {'$in': person_ids}})).count()
    auth_user.checked_stream = datetime.datetime.utcnow()
    session.commit()
    return stream_object_count