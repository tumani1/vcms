# coding: utf-8

from sqlalchemy import and_

from models import Extras, ExtrasTopics, UsersExtras, PersonsExtras, ExtrasMedia, ExtrasMediaUnits, Vars
from models.extras.constants import APP_EXTRA_TYPE_IMAGE


def get_content_users_info(pk, session, **kwargs):
    query = session.query(Extras).\
        join(UsersExtras, and_(Extras.id == UsersExtras.extra_id, UsersExtras.user_id == pk)).\
        filter(Extras.type == APP_EXTRA_TYPE_IMAGE).first()

    if not query is None:
        return {'location': query.location.strip()}

    query = session.query(Vars).filter(Vars.variable == 'default_user_pic').first()
    return {
        'location': query.text.strip() if not query is None and len(query.text) else '',
        'empty': True,
    }


def get_content_persons_info(pk, session, **kwargs):
    query = session.query(Extras).\
        join(PersonsExtras, and_(Extras.id == PersonsExtras.extras_id, PersonsExtras.person_id == pk)).\
        filter(Extras.type == APP_EXTRA_TYPE_IMAGE).first()

    if not query is None:
        return {'location': query.location.strip()}

    query = session.query(Vars).filter(Vars.variable == 'default_person_pic').first()
    return {
        'location': query.text.strip() if not query is None and len(query.text) else '',
        'empty': True,
    }


def get_content_topics_info(pk, session, **kwargs):
    query = session.query(Extras).\
        join(ExtrasTopics, and_(Extras.id == ExtrasTopics.extras_id, ExtrasTopics.topic_name == pk)).\
        filter(Extras.type == APP_EXTRA_TYPE_IMAGE).first()

    if not query is None:
        return {'location': query.location.strip()}

    query = session.query(Vars).filter(Vars.variable == 'default_topic_pic').first()
    return {
        'location':  query.text.strip() if not query is None and len(query.text) else '',
        'empty': True,
    }


def get_content_media_info(pk, session, **kwargs):
    query = session.query(Extras).\
        join(ExtrasMedia, and_(Extras.id == ExtrasMedia.extras_id, ExtrasMedia.media_id == pk)).\
        filter(Extras.type == APP_EXTRA_TYPE_IMAGE).first()

    if not query is None:
        return {'location': query.location.strip()}

    query = session.query(Vars).filter(Vars.variable == 'default_media_pic').first()
    return {
        'location': query.text.strip() if not query is None and len(query.text) else '',
        'empty': True,
    }


def get_content_mediaunits_info(pk, session, **kwargs):
    query = session.query(Extras).\
        join(ExtrasMediaUnits, and_(Extras.id == ExtrasMediaUnits.extras_id, ExtrasMediaUnits.mediaunit_id == pk)).\
        filter(Extras.type == APP_EXTRA_TYPE_IMAGE).first()

    if not query is None:
        return {'location': query.location.strip()}

    query = session.query(Vars).filter(Vars.variable == 'default_mediaunits_pic').first()
    return {
        'location': query.text.strip() if not query is None and len(query.text) else '',
        'empty': True,
    }
