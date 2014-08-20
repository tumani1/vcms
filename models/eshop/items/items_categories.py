# coding: utf-8

from sqlalchemy import Column, ForeignKey, Integer
from models import Base


class ItemsCategories(Base):
    __tablename__ = 'items_categories'

    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('items.id'), nullable=False)
    category_id = Column(ForeignKey('categories.id'), nullable=False)



    @classmethod
    def tmpl_for_items_categories(cls, session):
        query = session.query(cls)

        return query


    @classmethod
    def get_items_categories_by_category_id(cls, session, category_id):
        query = cls.tmpl_for_items_categories(session).filter_by(category_id=category_id)
        return query

    @classmethod
    def get_items_by_category_id(cls, session, category_id):
        query = cls.tmpl_for_items_categories(session).filter()