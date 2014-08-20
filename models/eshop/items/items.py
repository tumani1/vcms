# coding: utf-8
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, or_, and_, desc, asc, ForeignKey
from sqlalchemy.orm import relationship, contains_eager
from models import Base
from models.eshop.items.users_items import UsersItems
from models.eshop.items.items_objects import ItemsObjects
from models.eshop.items.items_extras import ItemsExtras


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    active = Column(Boolean, default=False)
    instock = Column(Boolean, default=False)
    added = Column(DateTime, nullable=True)
    price = Column(Float, nullable=True)
    price_old = Column(Float, nullable=True)
    is_digital = Column(Boolean, default=True)

    item_users = relationship('UsersItems', backref='items', cascade='all, delete')
    item_categories = relationship('ItemsCategories', backref='items', cascade='all, delete')
    item_extras = relationship('ItemsExtras', backref='items', cascade='all, delete')

    @classmethod
    def tmpl_for_items(cls, user, session):
        query = session.query(cls)

        query = query. \
            outerjoin(ItemsExtras, cls.id == ItemsExtras.item_id).\
            options(contains_eager(cls.item_extras))

        if not user is None:
            query = query. \
                outerjoin(UsersItems, and_(cls.id == UsersItems.item_id, UsersItems.user_id == user.id)).\
                options(contains_eager(cls.item_users))
        return query

    @classmethod
    def get_items_list(cls, user, session, id=None, limit=None, instock=None, name=None, text=None, price=None,
                       sort=None, sort_desc=None, is_watched=None, is_bought=None, cat=None, obj_type=None, obj_id=None, obj_name=None, is_digital=None, **kwargs):
        query = cls.tmpl_for_items(user, session)

        if not id is None:
            query = query.filter(cls.id.in_(id))

        if not instock is None:
            query = query.filter(cls.instock == instock)

        if not is_digital is None:
            if is_digital == True:
                query = query.filter(cls.is_digital == True)
            else:
                query = query.filter(cls.is_digital == False)

        if not name is None:
            query = query.filter(cls.name.like("%{0}%".format(name)))

        if not text is None:
            query = query.filter(or_(cls.name.like("%{0}%".format(text)), cls.description.like("%{0}%".format(text))))

        if not price is None:
            query = query.filter(and_(cls.price >= price[0], cls.price <= price[1]))

        if not sort is None:
            if sort == 'name':
                query = query.order_by(desc(cls.name) if sort_desc else asc(cls.name))
            elif sort == 'price':
                query = query.order_by(desc(cls.price) if sort_desc else asc(cls.price))
            elif sort == 'date':
                query = query.order_by(desc(cls.added) if sort_desc else asc(cls.added))

        if not cat is None:
            query = query.outerjoin(ItemsCategories).filter(ItemsCategories.category_id.in_(cat))

        if not obj_type is None:
            query = query.outerjoin(ItemsObjects).filter(ItemsObjects.obj_type == obj_type)

        if not obj_id is None:
            query = query.outerjoin(ItemsObjects).filter(ItemsObjects.obj_id == obj_id)

        if not obj_name is None:
            query = query.outerjoin(ItemsObjects).filter(ItemsObjects.obj_name == obj_name)

        if not user is None:
            if not is_watched is None:
                if is_watched == True:
                    query = query.filter(UsersItems.watched != None)
                else:
                    query = query.filter(UsersItems.watched == None)
            if not is_bought is None:
                if is_bought == True:
                    query = query.filter(UsersItems.bought_cnt > 0)
                else:
                    query = query.filter(or_(UsersItems.bought_cnt == 0, UsersItems.bought_cnt == None))

        total_cnt = len(query.all())

        # Set limit and offset filter
        if not limit is None:
            # Set Limit
            if limit[0]:
                query = query.limit(limit[0])

            # Set Offset
            if limit[1]:
                query = query.offset(limit[1])

        return query, total_cnt

    @classmethod
    def get_item_by_id(cls, user, session, item_id, **kwargs):
        query = cls.tmpl_for_items(user, session).filter(cls.id == item_id).first()
        return query


class ItemsCategories(Base):
    __tablename__ = 'items_categories'

    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('items.id'), nullable=False)
    category_id = Column(ForeignKey('categories.id'), nullable=False)

    category_items = relationship('Items', backref='items_categories', cascade='all, delete')

    @classmethod
    def tmpl_for_items_categories(cls, session):
        query = session.query(cls)

        return query

    @classmethod
    def get_items_categories_by_category_id(cls, session, category_id):
        query = cls.tmpl_for_items_categories(session).filter_by(category_id=category_id)
        return query

    @classmethod
    def get_item_by_category_id(cls, session, category_id):
        query = cls.tmpl_for_categories(session).filter(cls.category_id==category_id).outerjoin(Items, and_(cls.item_id==Items.id, Items.instock==True))

        return query