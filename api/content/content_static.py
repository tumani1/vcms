# coding: utf-8

from sqlalchemy import and_

from models import Extras, ExtrasTopics, UsersExtras, PersonsExtras, ExtrasMedia, ExtrasMediaUnits
from models.extras.constants import APP_EXTRA_TYPE_IMAGE


def get_content_users_info(pk, session, **kwargs):
    return "http://google.com"
    query = session.query(Extras).\
        outerjoin(UsersExtras, and_(Extras.id == UsersExtras.extra_id, UsersExtras.user_id == pk)).\
        filter(Extras.type == APP_EXTRA_TYPE_IMAGE).first()

    if not query is None:
        return query.location

    return ''


def get_content_persons_info(pk, session, **kwargs):
    query = session.query(Extras).\
        outerjoin(PersonsExtras, and_(Extras.id == PersonsExtras.extra_id, PersonsExtras.person_id == pk)).\
        filter(Extras.type == APP_EXTRA_TYPE_IMAGE).first()

    if not query is None:
        return query.location

    return ''


def get_content_topics_info(pk, session, **kwargs):
    return "http://google.com"

    query = session.query(Extras).\
        outerjoin(ExtrasTopics, and_(Extras.id == ExtrasTopics.extra_id, ExtrasTopics.topic_name == pk)).\
        filter(Extras.type == APP_EXTRA_TYPE_IMAGE).first()

    if not query is None:
        return query.location

    return ''


def get_content_media_info(pk, session, **kwargs):
    query = session.query(Extras).\
        outerjoin(ExtrasMedia, and_(Extras.id == ExtrasMedia.extra_id, ExtrasMedia.media_id == pk)).\
        filter(Extras.type == APP_EXTRA_TYPE_IMAGE).first()

    if not query is None:
        return query.location

    return ''


def get_content_mediaunits_info(pk, session, **kwargs):
    query = session.query(Extras).\
        outerjoin(ExtrasMediaUnits, and_(Extras.id == ExtrasMediaUnits.extra_id, ExtrasMediaUnits.mediaunit_id == pk)).\
        filter(Extras.type == APP_EXTRA_TYPE_IMAGE).first()

    if not query is None:
        return query.location

    return ''
