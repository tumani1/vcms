# coding: utf-8

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.event import listens_for

from models.mongo import Stream, constant
from models.base import Base


class PersonsMedia(Base):
    __tablename__ = 'persons_media'

    id        = Column(Integer, primary_key=True)
    media_id  = Column(Integer, ForeignKey('media.id'), nullable=False)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    role      = Column(String)
    type      = Column(String)

    def __repr__(self):
        return u"<PersonsMedia(id={0}, media={1}, person={2})>".format(self.id, self.media_id, self.person_id)


@listens_for(PersonsMedia, 'after_insert')
def create_media(target, **kwargs):
    Stream.signal(type_=constant.APP_STREAM_TYPE_PERS_O, object_={'media_id': target.media_id, 'person_id': target.person_id})