# coding: utf-8

from sqlalchemy import Column, Integer, String, Text, Index, DDL
from sqlalchemy.event import listen
from sqlalchemy_utils import ChoiceType, TSVectorType
from sqlalchemy_searchable import search

from models.base import Base
from utils.constants import OBJECT_TYPES


class Content(Base):
    __tablename__ = 'content'
    __table_args__ = (
        Index('content_search_name_gin_idx', 'search_name', postgresql_using='gin'),
    )

    id       = Column(Integer, primary_key=True)
    title    = Column(String, nullable=True)
    text     = Column(Text, nullable=True)
    obj_type = Column(ChoiceType(OBJECT_TYPES), nullable=False)
    obj_id   = Column(Integer, nullable=True)
    obj_name = Column(String, nullable=True)

    search_name = Column(TSVectorType('title', 'text', 'obj_name'))

    @classmethod
    def tmpl_for_content(cls, user, session):
        query = session.query(cls)

        if not user is None:
            pass

        return query

    @classmethod
    def get_content_list(cls, session, id=None, obj_type=None, obj_id=None, obj_name=None):
        query = session.query(cls)
        if id:
            query = query.filter(cls.id.in_(id))

        if obj_type:
            query = query.filter(cls.obj_type == obj_type)

            if obj_id:
                query = query.filter(cls.obj_id == obj_id)

            if obj_name:
                query = query.filter(cls.obj_name == obj_name)

        return query.all()

    @classmethod
    def get_search_by_text(cls, session, text, limit=None, **kwargs):
        query = cls.tmpl_for_content(None, session)

        # Full text search by text
        query = search(query, text)

        # Set limit and offset filter
        if not limit is None:
            # Set Limit
            if limit[0]:
                query = query.limit(limit[0])

            # Set Offset
            if limit[1]:
                query = query.offset(limit[1])

        return query

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

listen(Content, 'before_insert', validate_object)


update_media_units = DDL("""
CREATE FUNCTION content_update() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        new.search_name = to_tsvector('pg_catalog.english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.text, '') || ' ' || COALESCE(NEW.obj_name, ''));
    END IF;
    IF TG_OP = 'UPDATE' THEN
        IF NEW.title <> OLD.title OR NEW.text <> OLD.text OR NEW.obj_name <> OLD.obj_name THEN
            new.search_name =  to_tsvector('pg_catalog.english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.text, '') || ' ' || COALESCE(NEW.obj_name, ''));
        END IF;
    END IF;
    RETURN NEW;
END
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER content_search_name_update BEFORE INSERT OR UPDATE ON content
FOR EACH ROW EXECUTE PROCEDURE content_update();
""")

listen(Content.__table__, 'after_create', update_media_units)
