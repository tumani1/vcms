# coding: utf-8
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy_utils import ChoiceType
from models import Base
from utils.constants import OBJECT_TYPES
from sqlalchemy.event import listen


class TagsObjects(Base):
    __tablename__ = 'tags_objects'
    __jsonexport__ = ['tag_id', 'obj_type', 'obj_id', 'obj_type']

    id          = Column(Integer, primary_key=True)
    tag_id      = Column(Integer, ForeignKey('tags.id'), nullable=False, index=True)
    obj_type    = Column(ChoiceType(OBJECT_TYPES), nullable=False)
    obj_id      = Column(Integer)
    obj_name    = Column(String)
    
    def __repr__(self):
        return u'TagsObjects(name={0}, type={1}, obj_id={2},)'.format(self.obj_name, self.obj_type, self.obj_id)

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

listen(TagsObjects, 'before_insert', validate_object)