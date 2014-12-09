# coding: utf-8
from utils.connection import get_session
from models.media import Media, UsersMedia


# Подсчет рейтинга и кол-ва просмотров
def calc_media_rating_and_views():
    session = get_session()
    media = session.query(Media).all()

    for m in media:
        try:
            users_media = session.query(UsersMedia).filter(UsersMedia.media_id == m.id).all()
            views_cnt = 0
            rating = 0
            votes_cnt = 0

            for um in users_media:
                if um.views_cnt:
                    views_cnt += um.views_cnt
                if um.rating:
                    rating += um.rating
                    votes_cnt += 1

            if votes_cnt:
                rating /= votes_cnt

            m.views_cnt = views_cnt
            m.rating_votes = votes_cnt
            m.rating = rating
            session.commit()

        except Exception as e:
            print(e.message)
            session.rollback()