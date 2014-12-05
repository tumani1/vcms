# coding: utf-8
import requests
from models import Users, UsersSocial, GlobalToken, Extras, CDN, UsersExtras
from models.extras.constants import APP_EXTRA_TYPE_IMAGE
from models.users.constants import APP_USERSOCIAL_TYPE_OK, APP_USERS_GENDER_UNDEF,\
    APP_USERS_GENDER_MAN, APP_USERS_GENDER_WOMAN, APP_USER_STATUS_ACTIVE
from utils import NotAuthorizedException
from utils.avatar_save import save_avatar_to_file
from utils.constants import OK_SECRET_KEY, OK_CLIENT_ID, OK_REDIRECT_URI, OK_PUBLIC_KEY
import hashlib


def get(**kwargs):

    if 'meta' in kwargs:
        meta = kwargs['meta']

    # URL для открытия диалога
    url_auth_open_dialog = 'http://www.odnoklassniki.ru/oauth/authorize?' \
               'client_id={client_id}' \
               '&scope={scope}' \
               '&response_type=code' \
               '&redirect_uri={redirect}'

    url_auth_open_dialog = url_auth_open_dialog.format(client_id=OK_CLIENT_ID, scope='VALUABLE_ACCESS;GET_EMAIL', redirect=OK_REDIRECT_URI, )
    return {'redirect_url': url_auth_open_dialog, 'social': True}


def complete_get(auth_user, session, **kwargs):
    params = kwargs['query_params']

    if 'code' in params:
        code = params['code']
    else:
        raise NotAuthorizedException
    # URL получения access token
    url_get_access_token = 'https://api.odnoklassniki.ru/oauth/token.do'
    url_get_access_token_params = {
        'params': {
            'code': code,
            'client_id': OK_CLIENT_ID,
            'client_secret': OK_SECRET_KEY,
            'redirect_uri': OK_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
    }

    response = requests.post(url_get_access_token, **url_get_access_token_params)
    data = response.json()

    if 'error' in data:
        raise NotAuthorizedException

    access_token = data['access_token']

    # Формирование цифровой подписи
    ok_url_api_params = 'application_key={0}method=users.getCurrentUser'.format(OK_PUBLIC_KEY)
    md5_first_sig = hashlib.md5()
    first_sig = access_token + OK_SECRET_KEY
    md5_first_sig.update(first_sig)
    md5_first_param = md5_first_sig.hexdigest()
    ok_url_api_params += md5_first_param
    md5_second_sig = hashlib.md5()
    md5_second_sig.update(ok_url_api_params)

    # Цифровая подпись запроса к api одноклассников.ru
    sig = md5_second_sig.hexdigest()
    ok_params = {
        'params': {
            'application_key': OK_PUBLIC_KEY,
            'method': 'users.getCurrentUser',
            'access_token': access_token,
            'sig': sig,
        }
    }
    ok_get_user_req = 'http://api.odnoklassniki.ru/fb.do'

    # Данные о юзере
    user_data = requests.get(ok_get_user_req, **ok_params)
    user_data = user_data.json()

    user_id = user_data['uid']
    user_gender = APP_USERS_GENDER_UNDEF

    if user_data['gender'] == 'female':
        user_gender = APP_USERS_GENDER_WOMAN
    elif user_data['gender'] == 'male':
        user_gender = APP_USERS_GENDER_MAN

    users_social = session.query(UsersSocial).filter(UsersSocial.social_user_id == user_id).first()

    if not users_social is None:
        user = session.query(Users).filter(Users.id == users_social.user_id).first()
        return {'token': GlobalToken.generate_token(user.id, session), 'social_token': True}
    else:
        try:
            session.begin_nested() #SAVEPOINT

            user = Users(firstname=user_data['first_name'], lastname=user_data['last_name'], password=access_token, gender=user_gender, status=APP_USER_STATUS_ACTIVE)
            session.add(user)
            session.commit()

            avatar_path1 = save_avatar_to_file(user_data['pic_1'], 'photo', str(user.id))
            avatar_path2 = save_avatar_to_file(user_data['pic_2'], 'photo_max_orig', str(user.id))

            cdn = session.query(CDN).filter().first()

            extras1 = Extras(cdn_name=cdn.name, type=APP_EXTRA_TYPE_IMAGE, location=avatar_path1, description='', title='', title_orig='')
            extras2 = Extras(cdn_name=cdn.name, type=APP_EXTRA_TYPE_IMAGE, location=avatar_path2, description='', title='', title_orig='')
            session.add_all([extras1, extras2])
            session.commit()

            user_extras1 = UsersExtras(user_id=user.id, extra_id=extras1.id)
            user_extras2 = UsersExtras(user_id=user.id, extra_id=extras2.id)
            session.add_all([user_extras1, user_extras2])
            session.commit()

            users_social = UsersSocial(user_id=user.id, sType=APP_USERSOCIAL_TYPE_OK, sToken=' ', social_user_id=user_id)
            session.add(users_social)
            session.commit()

            return {'token': GlobalToken.generate_token(user.id, session), 'social_token': True}

        except Exception as e:
            print(e.message)
            session.rollback()
            raise NotAuthorizedException