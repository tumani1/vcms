# coding: utf-8

# from flask.ext import admin

from users_view import *
from tokens_view import *
from persons_view import *
from extras_view import *
from scheme_view import *
from topics_view import *
from chats_view import *
from locations_view import *
from stream_view import *
from media_view import *
from comments_view import *
from msgr_view import *
from tags_view import *
from content_view import *
from eshop_view import *
from admin_view import *

# import models
# ###############################################################################
# # Admin
# admin_view = admin.Admin(name='NextTV', index_view=AdminIndexView(), base_template='admin_master.html')
#
#
# from utils.connection import db_connect, sessionmaker
# from flask.ext.sqlalchemy import SQLAlchemy
# # from sqlalchemy.orm.session import Session as SessionBase
# from admin import session
# # from sqlalchemy.orm import Query
#
#
# class CustomAlchemy(SQLAlchemy):
#     def create_session(self, options):
#          return sessionmaker(**options)
#
# # session = CustomAlchemy(**{'session_options': {'bind': db_connect()}})
#
#
# ###############################################################################
# # Users
# admin_view.add_view(UsersModelView())
# admin_view.add_view(UsersRelsModelView())
# admin_view.add_view(UsersSocialModelView())
# admin_view.add_view(UsersValuesModelView())
# admin_view.add_view(UsersExtrasModelView())
# admin_view.add_view(UsersTopicsModelView())
#
# ###############################################################################
# # Token
# admin_view.add_view(SessionTokenModelView())
# admin_view.add_view(GlobalTokenModelView())
#
# ###############################################################################
# # Persons
# admin_view.add_view(PersonsModelView())
# # admin_view.add_view(PersonsValuesModelView())
# # admin_view.add_view(PersonsExtrasModelView())
# # admin_view.add_view(PersonsTopicsModelView())
#
# ###############################################################################
# # Topics
# admin_view.add_view(TopicsModelView())
# # admin_view.add_view(TopicsExtrasModelView())
#
# ###############################################################################
# # Chats
# admin_view.add_view(ChatsModelView())
# admin_view.add_view(UsersChatModelView())
# admin_view.add_view(ChatMessagesModelView())
#
# ###############################################################################
# # Contents
# admin_view.add_view(CitieModelView())
# admin_view.add_view(CountryModelView())
#
# ###############################################################################
# # Extras
# admin_view.add_view(ExtrasModelView())
#
# ###############################################################################
# # Scheme
# admin_view.add_view(SchemeModelView())
#
# ###############################################################################
# # CDN
# admin_view.add_view(CdnModelView())
#
# ###############################################################################
# # Stream
# admin_view.add_view(StreamModelView())
#
# ###############################################################################
# # Media
# admin_view.add_view(MediaModelView())
# admin_view.add_view(MediaUnitsModelView())
# admin_view.add_view(MediaInUnitModelView())
# admin_view.add_view(PersonsMediaModelView())
# admin_view.add_view(UsersMediaModelView())
# admin_view.add_view(UsersMediaUnitsModelView())
# admin_view.add_view(MediaLocationsModelView())
# admin_view.add_view(MediaAccessCountriesModelView())
# admin_view.add_view(MediaAccessDefaultsModelView())
# admin_view.add_view(MediaAccessDefaultsCountriesModelView())
# admin_view.add_view(MediaUnitsAccessCountriesModelView())
#
# ###############################################################################
# # Comments
# admin_view.add_view(CommentsModelView())
#
# ###############################################################################
# # Msgr
# admin_view.add_view(MsgrLogModelView())
# admin_view.add_view(MsgrThreadsModelView())
# admin_view.add_view(UsersMsgrThreadsModelView())
#
# ###############################################################################
# # Tags
# admin_view.add_view(TagsModelView())
# admin_view.add_view(TagsObjectsModelView())
#
# ###############################################################################
# # Content
# admin_view.add_view(ContentModelView())
#
# ###############################################################################
# # Eshop
# admin_view.add_view(ItemsModelView())
# admin_view.add_view(ItemsExtrasModelView())
# admin_view.add_view(ItemsObjectsModelView())
# admin_view.add_view(UsersItemsModelView())
# admin_view.add_view(CategoriesModelView())
# admin_view.add_view(CategoriesExtrasModelView())
# admin_view.add_view(VariantsModelView())
# admin_view.add_view(VariantsExtrasModelView())
# admin_view.add_view(VariantsSchemeModelView())
# admin_view.add_view(VariantsValuesModelView())
# admin_view.add_view(CartsModelView())
# admin_view.add_view(CartLogModelView())
# admin_view.add_view(ItemsCartsModelView())
# admin_view.add_view(PaymentsModelView())
