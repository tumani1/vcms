# coding: utf-8
from models.locations import Countries
from models.media.constants import APP_ACCESS_LEVEL_MANAGER_MASK,\
    APP_ACCESS_LEVEL_OWNER_MASK, APP_ACCESS_LEVEL_GUEST_MASK,\
    APP_ACCESS_LEVEL_AUTH_USER_MASK, APP_MEDIA_TYPE_DEFAULT
from models.media import MediaAccessCountries, MediaAccessDefaultsCountries,\
    MediaAccessDefaults, MediaUnitsAccessCountries, MediaUnits, MediaInUnit, Media

from utils.constants import HTTP_OK, HTTP_INTERNAL_SERVER_ERROR


def user_access(user, media, session):
    access = media.access

    if access is None:
        pass

    if access is None:
        access = session.query(MediaAccessDefaults.access).filter_by(name=media.type_.code).scalar()

    if access is None:
        access = session.query(MediaAccessDefaults.access).filter_by(name=APP_MEDIA_TYPE_DEFAULT).scalar()

    status_code = HTTP_INTERNAL_SERVER_ERROR

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


def geo_access(ip_address, media, session, reader):
    country_name = reader.country(ip_address).country.iso_code
    country = session.query(Countries).filter_by(id=country_name).first()

    status_code = MediaAccessCountries.access_media(media, country, session)

    if status_code is None:
        media_units = session.query(MediaUnits).join(MediaInUnit).join(Media).filter(Media.id == media.id).all()
        status_code = MediaUnitsAccessCountries.access_media_unit(media_units, country, session)

    if status_code is None:
        status_code = MediaAccessDefaultsCountries.access_media_type(media.type_.code, country, session)

    if status_code is None:
        status_code = MediaAccessDefaultsCountries.access_media_type(APP_MEDIA_TYPE_DEFAULT, country, session)

    if status_code is None:
        status_code = HTTP_OK

    return status_code


def access(user, ip_address, media, session, reader):
    status_code = user_access(user, media, session)
    if status_code == HTTP_OK:
        status_code = geo_access(ip_address, media, session, reader)

    return status_code

