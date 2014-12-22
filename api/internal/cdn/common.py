# coding: utf-8
from models.locations import Countries
from models.media.constants import APP_MEDIA_TYPE_DEFAULT
from models.media import MediaAccessCountries, MediaAccessDefaultsCountries,\
    MediaAccessDefaults, MediaUnitsAccessCountries, MediaUnits, MediaInUnit, Media

from utils.constants import HTTP_OK


def user_access(user, media, session):
    owner = user == media.users_media
    is_auth = True if user else False
    is_manager = True if user and user.is_manager else False

    status_code = Media.access_media(media, owner, is_auth, is_manager)
    if status_code is None:
        media_units = session.query(MediaUnits).join(MediaInUnit).join(Media).filter(Media.id == media.id).all()
        status_code = MediaUnits.access_media_units(media_units, owner, is_auth, is_manager)

    if status_code is None:
        status_code = MediaAccessDefaults.access_media_type(media.type_, owner, is_auth, is_manager, session)

    if status_code is None:
        status_code = MediaAccessDefaults.access_media_type(APP_MEDIA_TYPE_DEFAULT, owner, is_auth, is_manager, session)

    if status_code is None:
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
