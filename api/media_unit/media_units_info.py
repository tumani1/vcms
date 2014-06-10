from models import db
from models.media.media_units import MediaUnits
from serializer import mMediaUnitsSerializer


@db
def get(user, session, id, **kwargs):
    instance = MediaUnits.get_media_unit_by_name(user, session, id)
    params = {
        'instance': instance,
        'user': user,
        'session': session,
    }
    return mMediaUnitsSerializer(**params).data
