# coding: utf-8
from models import News
from utils.validation import validate_int


def get(news_id, auth_user, session, **kwargs):
    data = {}

    news_id = validate_int(news_id, min_value=1)
    instance = News.get_news_by_id(session, news_id)

    if not instance is None:
        params = {
            'instance': instance,
            'user': auth_user,
            'session': session,
        }
    #To do
    return data


