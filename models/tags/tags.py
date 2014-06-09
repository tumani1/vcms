class Tags(Base):
    __tablename__ = 'tags'
    __jsonexport__ = ['name','status','type']

    
    name    = Column(String)
    status  = Column(String)
    type    = Column(String)
    
    def __repr__(self):
        return u'Tags(name={0}, status={1}, type={2},)'.format(self.name, self.status, self.type)
