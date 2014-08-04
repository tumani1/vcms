# coding: utf-8
from models.comments.comments import Comments
from utils.validation import validate_int, validate_string, validate_obj_type
import datetime


def post(auth_user, session, text, **kwargs):
    text = validate_string(text)
    date = datetime.datetime.now()
    params = {
        'user_id': auth_user.id,
        'text': text,
        'created': date
    }

    if 'parent_id' in kwargs['query']:
        parent_id = validate_int(kwargs['query']['parent_id'], min_value=1)
        parent = Comments.get_comment_by_id(auth_user, session, parent_id)
        if parent:
            params.update(parent_id=parent_id, obj_type=parent.obj_type.code)
            if parent.obj_id:
                params.update(obj_id=parent.obj_id)
            else:
                params.update(obj_name=parent.obj_name)
            new_comment = Comments(**params)

    else:
        obj_type = validate_obj_type(kwargs['query']['obj_type'])
        if 'obj_id' in kwargs['query']:
            obj_id = validate_int(kwargs['query']['obj_id'], min_value=1)
            params.update(obj_type=obj_type, obj_id=obj_id)
        else:
            obj_name = validate_string(kwargs['query']['obj_name'])
            params.update(obj_type=obj_type, obj_name=obj_name)
        new_comment = Comments(**params)

    session.add(new_comment)
    if session.new:
        session.commit()


def delete(auth_user, session, id, **kwargs):
    pass
