# coding: utf-8
from sqlalchemy import Column, Integer, String
from models import Base, Extras
from models.eshop.categories.categories_extras import CategoriesExtras


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(Integer, nullable=True)

    @classmethod
    def tmpl_for_categories(cls, session):
        query = session.query(cls)

        return query

    @classmethod
    def get_categories_by_id(cls, session, categories_id):
        query = cls.tmpl_for_categories(session).filter_by(id=categories_id)
        return query

    @classmethod
    def get_item_by_category_id(cls, session, category_id):
        sql = " join items_categories on categories.id = 1 " \
              "join  items on (items_categories.item_id = items.id and items.instock=True)"
        query = cls.tmpl_for_categories(session).filter(sql)

        return query

    @classmethod
    def get_extras_by_category_id(cls, session, category_id):
        query = cls.tmpl_for_categories(session).\
            outerjoin(CategoriesExtras, category_id==CategoriesExtras.categories_id).\
            outerjoin(Extras, Extras.id==CategoriesExtras.extras_id)
        return query

