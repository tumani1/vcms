# coding: utf-8
from sqlalchemy import Column, Integer, String, func, asc
from sqlalchemy.orm import relationship
from models.eshop.items import ItemsCategories
from models.eshop.items.items import Items
from models import Base


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)

    category_extras = relationship('CategoriesExtras', backref='categories', cascade='all, delete')
    category_variants_schemes = relationship('VariantsScheme', backref='categories', cascade='all, delete')

    items_categories = relationship('ItemsCategories', backref='categories', cascade='all, delete')

    @classmethod
    def tmpl_for_categories(cls, session):
        query = session.query(Categories.id, Categories.name, Categories.description)

        return query

    @classmethod
    def get_categories_by_id(cls, session, categories_id):
        query = cls.tmpl_for_categories(session).filter_by(id=categories_id)
        return query

    @classmethod
    def get_list_categories(cls, session, instock=None, has_items=None, sort=None):
        query = cls.tmpl_for_categories(session).\
            outerjoin(ItemsCategories, cls.id==ItemsCategories.category_id)

        if not has_items is None:
            if not has_items:
                query = cls.tmpl_for_categories(session).\
                    outerjoin(ItemsCategories, cls.id == ItemsCategories.category_id)

                query = query.outerjoin(Items, ItemsCategories.item_id == Items.id).\
                    filter(ItemsCategories.item_id == None)
            else:
                query = query.outerjoin(Items, ItemsCategories.item_id==Items.id).\
                    filter(ItemsCategories.item_id != None)

        if not instock is None:
            query = query.outerjoin(Items, ItemsCategories.item_id==Items.id).\
                filter(ItemsCategories.item_id != None)
            if instock:
                query = query.filter(Items.instock==True)
            else:
                query = query.filter(Items.instock==False)

        if not sort is None:
            if sort == 'name':
                query = query.order_by(asc(cls.name))
            else:
                query = query.\
                    order_by(asc(func.count(ItemsCategories.item_id)))

        return query.group_by(Categories.id)


