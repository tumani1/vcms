# coding: utf-8
from sqlalchemy import Column, SMALLINT, DDL
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from models.base import Base
from models.media.constants import APP_MEDIA_TYPE, APP_MEDIA_TYPE_AUDIO,\
    APP_MEDIA_TYPE_PICTURE, APP_MEDIA_TYPE_VIDEO


class MediaType(Base):
    __tablename__ = 'media_type'

    type_        = Column(ChoiceType(APP_MEDIA_TYPE), primary_key=True)
    access_level = Column(SMALLINT, default=None, nullable=True)

    medias = relationship('Media', backref='media_type', cascade='all, delete')


create_rows = DDL("""INSERT INTO "media_type" VALUES('{audio}', NULL), ('{video}', NULL), ('{picture}', NULL);""".
                  format(audio=APP_MEDIA_TYPE_AUDIO, video=APP_MEDIA_TYPE_VIDEO,
                         picture=APP_MEDIA_TYPE_PICTURE))
listen(MediaType.__table__, 'after_create', create_rows)