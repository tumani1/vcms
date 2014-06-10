# coding: utf-8
from sqlalchemy import Column,Integer,String
from models import Base

class Tags(Base):
    __tablename__ = 'tags'
    __jsonexport__ = ['name','status','type']

    id = Column(Integer,primary_key = True,index = True)    
    name    = Column(String)
    status  = Column(String)
    type    = Column(String)
    
    def __repr__(self):
        return u'Tags(name={0}, status={1}, type={2},)'.format(self.name, self.status, self.type)
