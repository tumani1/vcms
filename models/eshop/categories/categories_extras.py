# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey
from models import Base, Categories


class CategoriesExtras(Base):
    __tablename__ = 'categories_extras'

    id = Column(Integer, primary_key=True)
    categories_id = Column(ForeignKey('categories.id'), nullable=False)
    extras_id = Column(ForeignKey('extras.id'), nullable=False)
    extras_type = Column(Integer, nullable=True)

    @classmethod
    def tmpl_for_categories(cls, session):
        query = session.query(cls)

        return query

    @classmethod
    def get_extras_by_category_id(cls, session, category_id):
        query = cls.tmpl_for_categories(session).outerjoin(Categories, )
