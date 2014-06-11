from models import db, MediaUnits
from api.media_unit.serializer import mMediaUnitsSerializer


@db
def get(user, session, id, **kwargs):
    instance = MediaUnits.get_prev_media_unit(user, session, id)
    data = {}
    if not instance is None:
        params = {
            'instance': instance,
            'user': user,
            'session': session,
        }
        data = mMediaUnitsSerializer(**params).data
    return data