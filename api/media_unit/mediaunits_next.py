from models import MediaUnits
from db_engine import db
from api.media_unit.serializer import mMediaUnitsSerializer


@db
def get(user, session, id, **kwargs):
    instance = MediaUnits.get_next_media_unit(user, session, id)
    data = {}
    if not instance is None:
        params = {
            'instance': instance,
            'user': user,
            'session': session,
        }
        data = mMediaUnitsSerializer(**params).data
    return data
