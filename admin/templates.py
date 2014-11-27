# coding: utf-8

from jinja2 import Markup

from flask import url_for


DROPDOWN_TEMPLATE = u"""
<div class="btn-group">
  <button class="btn dropdown-toggle" data-toggle="dropdown"><span class="caret"></span></button>
  <ul class="dropdown-menu">%s</ul>
</div>
"""

UL_TEMPLATE = u"<li><a href='%s'>%s</a></li>"


def topic_link_formatter(view, context, model, name):
    action = [
        UL_TEMPLATE % (url_for('mediaunits.index_view', flt1_0=model.name), u'Медиа'),
    ]

    return Markup(DROPDOWN_TEMPLATE % ''.join(action))


def person_link_formatter(view, context, model, name):
    action = [
        UL_TEMPLATE % (url_for('users.index_view', flt1_0=model.id), u'Роли'),
    ]

    return Markup(DROPDOWN_TEMPLATE % ''.join(action))


def user_link_formatter(view, context, model, name):
    action = [
        UL_TEMPLATE % (url_for('comments.index_view', flt1_0=model.id), u'Комментарии'),
        UL_TEMPLATE % (url_for('chats.index_view', flt1_0=model.id), u'Сообщения в чате')
    ]

    if False:
        action.append(UL_TEMPLATE % (url_for('persons.index_view', flt1_0=model.id), u'Персона'))

    return Markup(DROPDOWN_TEMPLATE % ''.join(action))


def media_link_formatter(view, context, model, name):
    action = [
        UL_TEMPLATE % (url_for('medialocations.index_view'), u'Локации'),
    ]

    return Markup(DROPDOWN_TEMPLATE % ''.join(action))
