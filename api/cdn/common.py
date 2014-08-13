# coding: utf-8
from models.locations import Countries
from models.media.constants import APP_ACCESS_LEVEL_MANAGER_MASK,\
    APP_ACCESS_LEVEL_OWNER_MASK, APP_ACCESS_LEVEL_GUEST_MASK,\
    APP_ACCESS_LEVEL_AUTH_USER_MASK, APP_MEDIA_TYPE_DEFAULT, APP_MEDIA_ACCESS_LIST
from models.media import MediaAccessCountries, MediaAccessDefaultsCountries,\
    MediaAccessDefaults
from utils.constants import HTTP_OK, HTTP_FORBIDDEN
from settings import GEO_IP_DATABASE

from geoip2 import database


def user_access(user, media, session):
    access = media.access

    # TODO: media-unit
    if access is None:
        pass

    if access is None:
        access = session.query(MediaAccessDefaults.access).filter_by(name=media.type_.code).first()

    if access is None:
        access = session.query(MediaAccessDefaults.access).filter_by(name=APP_MEDIA_TYPE_DEFAULT).first()

    status_code = HTTP_FORBIDDEN

    if access is None:
        status_code = HTTP_OK
    elif user:
        if user == media.user_owner and (access & APP_ACCESS_LEVEL_OWNER_MASK) != 0:
            status_code = HTTP_OK
        elif user.is_manager and (access & APP_ACCESS_LEVEL_MANAGER_MASK) != 0:
            status_code = HTTP_OK
        elif (access & APP_ACCESS_LEVEL_AUTH_USER_MASK) != 0:
            status_code = HTTP_OK
    elif (access & APP_ACCESS_LEVEL_GUEST_MASK) != 0:
        status_code = HTTP_OK

    return status_code


def geo_access(ip_address, media, session):
    reader = database.Reader(GEO_IP_DATABASE)
    try:
        country_name = reader.country(ip_address)
    except Exception as e:
        if media.access_type == APP_MEDIA_ACCESS_LIST:
            return HTTP_OK
        else:
            return HTTP_FORBIDDEN
    country = session.query(Countries).filte_by(name=country_name).first()

    status_code = MediaAccessCountries.access_media(media, country, session)
    # TODO: media-units
    if status_code is None:
        pass

    if status_code is None:
        status_code = MediaAccessDefaultsCountries.access_media_type(media.type_, country, session)

    if status_code is None:
        status_code = HTTP_OK

    return status_code


def access(user, ip_address, media, session):
    status_code = user_access(user, media, session)
    if status_code == HTTP_OK:
        status_code = geo_access(ip_address, media, session)
    return status_code

