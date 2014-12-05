#coding:utf-8
from utils import need_authorization
from models.extras import Extras
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
            e = Extras(type=APP_EXTRA_TYPE_IMAGE, title=filename, title_orig=filename,
                            description='avatar', location=auth_user.id, cdn_name=cdn.name)
            session.add(e)
            session.commit()
        else:
            raise RequestErrorException
    else:
        raise RequestErrorException