#coding:utf-8
from os.path import join
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
        location = join(str(auth_user.id), filename)
        if cdn:
            e = session.query(Extras).filter_by(type=APP_EXTRA_TYPE_IMAGE, location=location, cdn_name=cdn.name).first()
            if not e:
                e = Extras(type=APP_EXTRA_TYPE_IMAGE, title='', title_orig='',
                           description='', location=location, cdn_name=cdn.name)
            session.add(e)
            session.commit()
            ue = UsersExtras(user_id=auth_user.id, extra_id=e.id)
            session.add(ue)
            session.commit()
        else:
            raise RequestErrorException
    else:
        raise RequestErrorException