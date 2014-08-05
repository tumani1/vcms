# coding: utf-8

from api.serializers import mCommentSerializer
from models.comments.comments import Comments
from utils.validation import validate_int


def get(id, auth_user, session, **kwargs):
    comment_id = validate_int(id)
    instance = Comments.get_comment_by_id(auth_user, session, comment_id)
    if not instance is None:
        params = {
            'instance': instance,
            'user': auth_user,
            'session': session,
        }
        data = mCommentSerializer(**params).data
    return data
