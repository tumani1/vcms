# coding: utf-8

from sqlalchemy import Column, ForeignKey, Integer, String
from models import Base
from sqlalchemy.event import listen
from sqlalchemy_utils import ChoiceType
from models.comments.constants import OBJECT_TYPES


class ItemsObjects(Base):
    __tablename__ = 'items_objects'


    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('items.id'), nullable=False)
    obj_type = Column(ChoiceType(OBJECT_TYPES), nullable=False)
    obj_id = Column(Integer, nullable=True)
    obj_name = Column(String, nullable=True)

    def validate_obj(self):
        count = 0
        if self.obj_id:
            count += 1
        elif self.obj_name:
            count += 1

        if not count:
            raise ValueError(u'Необходимо указать obj_id или obj_name')
        return self


def validate_object(mapper, connect, target):
    target.validate_obj()

listen(ItemsObjects, 'before_insert', validate_object)