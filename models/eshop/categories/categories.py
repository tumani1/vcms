# coding: utf-8
from sqlalchemy import Column, Integer, String, desc
from models.eshop.items import ItemsCategories
from models.eshop.items.items import Items
from models import Base


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
    def get_list_categories(cls, session, instock=None, has_items=None, sort=None):
        query = cls.tmpl_for_categories(session).\
            outerjoin(ItemsCategories, cls.id==ItemsCategories.category_id).\
                    outerjoin(Items, ItemsCategories.item_id==Items.id).filter(ItemsCategories.item_id != None)

        if not has_items is None:
            if not has_items:
                query = query.outerjoin(ItemsCategories, cls.id==ItemsCategories.category_id).\
                    outerjoin(Items, ItemsCategories.item_id==Items.id).filter(ItemsCategories.item_id == None)

        if not instock is None and has_items!=False:
            if instock:
                query = query.filter(Items.instock==True)

        if not sort is None:
            if sort == 'name':
                query = query.order_by(desc(cls.name))
            else:
                query = query

        return query


