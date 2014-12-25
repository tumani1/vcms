#coding:utf-8
from utils import need_authorization
from models.extras import Extras
from models.users import UsersExtras
from models.cdn import CDN
from models.extras.constants import APP_EXTRA_TYPE_IMAGE
from utils.exceptions import RequestErrorException


@need_authorization
def post(session, auth_user, **kwargs):
    qp = kwargs['query_params']
    filename = qp.get('filename')

    if filename:
        cdn = session.query(CDN).first()
        if cdn:
            sub = session.query(UsersExtras.extra_id).filter_by(user_id=auth_user.id).subquery()
            e = session.query(Extras).filter(Extras.id.in_(sub.c)).filter_by(type=APP_EXTRA_TYPE_IMAGE,
                                                                             location=filename, cdn_name=cdn.name).first()
            if not e:
                e = Extras(type=APP_EXTRA_TYPE_IMAGE, title='', title_orig='',
                           description='', location=filename, cdn_name=cdn.name)
                session.add(e)
                session.commit()
                ue = UsersExtras(user_id=auth_user.id, extra_id=e.id)
                session.add(ue)
                session.commit()
        else:
            raise RequestErrorException
    else:
        raise RequestErrorException