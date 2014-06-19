from db_engine import db
from models.media.media_units import MediaUnits
from serializer import mMediaUnitsSerializer


@db
def get(user, session, id, **kwargs):
    data = {}
    instance = MediaUnits.get_media_unit_by_id(user, session, id)
    if not instance is None:
        params = {
            'instance': instance,
            'user': user,
            'session': session,
        }
        data = mMediaUnitsSerializer(**params).data
    return data
