# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, and_
from sqlalchemy.orm import relationship, contains_eager
from models import Base, Extras


class CategoriesExtras(Base):
    __tablename__ = 'categories_extras'

    id = Column(Integer, primary_key=True)
    categories_id = Column(ForeignKey('categories.id'), nullable=False)
    extras_id = Column(ForeignKey('extras.id'), nullable=False)
    extras_type = Column(Integer, nullable=True)

    extras = relationship('Extras', backref='categories_extras', cascade='all, delete')

    @classmethod
    def tmpl_for_categories(cls, session):
        query = session.query(cls)

        return query

    @classmethod
    def join_with_extras(cls, session, category_id):
        query = cls.tmpl_for_categories(session).filter(cls.categories_id==category_id)\
            .outerjoin(Extras, Extras.id==cls.extras_id).options(contains_eager(cls.extras))
        return query