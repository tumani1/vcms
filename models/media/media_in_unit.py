# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base


class MediaInUnit(Base):
    __tablename__ = 'media_in_unit'

    id            = Column(Integer, primary_key=True)
    media_id      = Column(Integer, ForeignKey('media.id'), nullable=False)
    media_unit_id = Column(Integer, ForeignKey('media_units.id'), nullable=False)
    m_order       = Column(Integer, nullable=True)

    def __repr__(self):
        return u'<MediaInUnit(id={0}, media={1}, media_unit={2})>'.format(self.id, self.media_id, self.media_unit_id)