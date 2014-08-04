# coding: utf-8
from models.cdn import CDN


def cdn_list(session, **kwargs):
    return session.query(CDN.url).all()
