# coding: utf-8
from flask import redirect, request, url_for
from flask.ext import admin, login
from flask.ext.admin import expose, helpers
from admin.forms import LoginForm

from users import UsersRelsModelView, UsersModelView, UsersValuesModelView,\
    UsersSocialModelView, UsersExtrasModelView, UsersTopicsModelView
from tokens import SessionTokenModelView, GlobalTokenModelView
from persons import PersonsModelView, PersonsUsersModelView,\
    PersonsValuesModelView, PersonsExtrasModelView, PersonsTopicsModelView
from extras import ExtrasModelView
from scheme import SchemeModelView
from topics import TopicsModelView, TopicsExtrasModelView
from cdn import CdnModelView
from chats import ChatsModelView, UsersChatModelView, ChatMessagesModelView
from locations import CountryModelView, CitieModelView
from stream import StreamModelView
from media import MediaModelView, MediaUnitsModelView, MediaInUnitModelView, PersonsMediaModelView,\
    UsersMediaModelView, UsersMediaUnitsModelView, MediaLocationsModelView, MediaAccessCountriesModelView,\
    MediaAccessDefaultsModelView, MediaAccessDefaultsCountriesModelView, MediaUnitsAccessCountriesModelView
from comments import CommentsModelView, UsersCommentsModelView
from msgr import MsgrLogModelView, MsgrThreadsModelView, UsersMsgrThreadsModelView
from tags import TagsModelView, TagsObjectsModelView
from content import ContentModelView


class AdminIndexView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(AdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST', ))
    def login_view(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)
        if login.current_user.is_authenticated():
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(AdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

admin_view = admin.Admin(name='NextTV', index_view=AdminIndexView(), base_template='admin_master.html')

###############################################################################
# Users

admin_view.add_view(UsersModelView())
admin_view.add_view(UsersRelsModelView())
admin_view.add_view(UsersSocialModelView())
admin_view.add_view(UsersValuesModelView())
admin_view.add_view(UsersExtrasModelView())
admin_view.add_view(UsersTopicsModelView())
###############################################################################

###############################################################################
# Token

admin_view.add_view(SessionTokenModelView())
admin_view.add_view(GlobalTokenModelView())
###############################################################################

###############################################################################
# Persons

admin_view.add_view(PersonsModelView())
admin_view.add_view(PersonsUsersModelView())
admin_view.add_view(PersonsValuesModelView())
admin_view.add_view(PersonsExtrasModelView())
admin_view.add_view(PersonsTopicsModelView())
###############################################################################

###############################################################################
# Topics

admin_view.add_view(TopicsModelView())
admin_view.add_view(TopicsExtrasModelView())
###############################################################################

###############################################################################
# Chats

admin_view.add_view(ChatsModelView())
admin_view.add_view(UsersChatModelView())
admin_view.add_view(ChatMessagesModelView())
###############################################################################

###############################################################################
# Contents

admin_view.add_view(CitieModelView())
admin_view.add_view(CountryModelView())
###############################################################################

###############################################################################
# Extras

admin_view.add_view(ExtrasModelView())
###############################################################################

###############################################################################
# Scheme

admin_view.add_view(SchemeModelView())
###############################################################################

###############################################################################
# CDN

admin_view.add_view(CdnModelView())
###############################################################################

###############################################################################
# Stream

admin_view.add_view(StreamModelView())
###############################################################################

###############################################################################
# Media

admin_view.add_view(MediaModelView())
admin_view.add_view(MediaUnitsModelView())
admin_view.add_view(MediaInUnitModelView())
admin_view.add_view(PersonsMediaModelView())
admin_view.add_view(UsersMediaModelView())
admin_view.add_view(UsersMediaUnitsModelView())
admin_view.add_view(MediaLocationsModelView())
admin_view.add_view(MediaAccessCountriesModelView())
admin_view.add_view(MediaAccessDefaultsModelView())
admin_view.add_view(MediaAccessDefaultsCountriesModelView())
admin_view.add_view(MediaUnitsAccessCountriesModelView())
###############################################################################

###############################################################################
# Comments

admin_view.add_view(CommentsModelView())
admin_view.add_view(UsersCommentsModelView())
###############################################################################

###############################################################################
# Msgr

admin_view.add_view(MsgrLogModelView())
admin_view.add_view(MsgrThreadsModelView())
admin_view.add_view(UsersMsgrThreadsModelView())
###############################################################################

###############################################################################
# Tags

admin_view.add_view(TagsModelView())
admin_view.add_view(TagsObjectsModelView())
###############################################################################

###############################################################################
# Content

admin_view.add_view(ContentModelView())
###############################################################################