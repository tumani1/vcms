from api.comments.serializer.m_comment import mCommentSerializer
from models.comments.comments import Comments
from utils.validation import validate_int


def get(auth_user, session, id, **kwargs):
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