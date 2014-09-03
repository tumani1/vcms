# coding: utf-8
import datetime

from api.serializers import mCommentSerializer
from models.mongo import Stream, constant
from models.comments.comments import Comments
from utils import need_authorization
from utils.validation import validate_int, validate_string, validate_obj_type
from utils.exceptions import RequestErrorException


@need_authorization
def post(auth_user, session, **kwargs):
    if 'text' in kwargs['query_params']:
        text = validate_string(kwargs['query_params']['text'])
    else:
        raise RequestErrorException
    date = datetime.datetime.now()
    params = {
        'user_id': auth_user.id,
        'text': text,
        'created': date
    }

    if 'parent_id' in kwargs['query_params']:
        parent_id = validate_int(kwargs['query_params']['parent_id'], min_value=1)
        parent = Comments.get_comment_by_id(auth_user, session, parent_id)
        if parent:
            params.update(parent_id=parent_id, obj_type=parent.obj_type.code)
            if parent.obj_id:
                params.update(obj_id=parent.obj_id)
            else:
                params.update(obj_name=parent.obj_name)
            new_comment = Comments(**params)

    else:
        obj_type = validate_obj_type(kwargs['query_params']['obj_type'])
        if 'obj_id' in kwargs['query_params']:
            obj_id = validate_int(kwargs['query_params']['obj_id'], min_value=1)
            params.update(obj_type=obj_type, obj_id=obj_id)
        else:
            obj_name = validate_string(kwargs['query_params']['obj_name'])
            params.update(obj_type=obj_type, obj_name=obj_name)
        new_comment = Comments(**params)

    session.add(new_comment)
    if session.new:
        session.commit()

    Stream.signal(type_=constant.APP_STREAM_TYPE_MEDIA_C, object_={'comment_id': new_comment.id}, user_id=auth_user.id)
    return mCommentSerializer(instance=new_comment, user=auth_user, session=session)


def delete(auth_user, session, id, **kwargs):
    pass
