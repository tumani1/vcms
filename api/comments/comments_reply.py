# coding: utf-8
from comments_create import post as create_comment


def post(id, auth_user, session, text, **kwargs):
    return create_comment(auth_user, session, text, parent_id=id)
