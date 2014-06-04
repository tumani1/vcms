# coding: utf-8

from models import db, Topics

@db
def get_topics_info(name, session=None):
    instance = session.query(Topics)
