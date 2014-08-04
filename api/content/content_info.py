# coding=utf-8

from models.content import Content
from api.serializers import mContentSerializer


def get_content_info(auth_user, session, **kwargs):

    content = kwargs['content']
    c = session.query(Content).get(content)
    data = mContentSerializer(c).get_data()
    return data
