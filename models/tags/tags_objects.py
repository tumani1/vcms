# coding: utf-8
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from models import Base


class TagsObjects(Base):
    __tablename__ = 'tags_objects'
    __jsonexport__ = ['tag_id', 'obj_type','obj_id','obj_type']

    id          = Column(Integer, primary_key=True)
    tag_id      = Column(Integer,ForeignKey('tags.id'),nullable = False, index =True)
    obj_type    = Column(String)
    obj_id      = Column(Integer)
    obj_name    = Column(String)
    
    def __repr__(self):
        return u'TagsObjects(name={0}, type={1}, obj_id={2},)'.format(self.obj_name, self.obj_type, self.obj_id)




                                                                      
