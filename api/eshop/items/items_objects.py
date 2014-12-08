# coding: utf-8
from api.serializers import mMediaUnitsSerializer, mMediaSerializer, mPersonSerializer, mContentSerializer, \
    mStreamElement
from models import MediaUnits, Media, Persons, Stream, Content
from models.eshop.items.items import Items
from utils.validation import validate_int


def get(item_id, auth_user, session, **kwargs):
    object_types = {
            'mu': (MediaUnits, mMediaUnitsSerializer),
            'm': (Media, mMediaSerializer),
            'p': (Persons, mPersonSerializer),
            'c': (Content, mContentSerializer),
            's': (Stream, mStreamElement),
    }
    data = []
    item_id = validate_int(item_id, min_value=1)
    item = Items.get_item_by_id(auth_user, session, item_id)
    if not item is None:
        for obj in item.item_objects:
            obj_class = object_types[obj.obj_type.code][0]
            if obj.obj_id:
                if obj.obj_type.code == 's':
                    object_ = obj_class.objects.get(id=obj.obj_id)
                else:
                    object_ = session.query(obj_class).filter(obj_class.id == obj.obj_id).first()
            elif obj.obj_name:
                object_ = session.query(obj_class).filter(obj_class.name == obj.obj_name).first()
            if obj.obj_type.code == 'c':
                data.append(object_types[obj.obj_type.code][1](object_).get_data())
            else:
                params = {
                    'instance': object_,
                    'user': auth_user,
                    'session': session,
                }
                data.append(object_types[obj.obj_type.code][1](**params).data)
    return data
