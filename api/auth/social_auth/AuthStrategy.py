from social.strategies.base import BaseStrategy, BaseTemplateStrategy


class AuthTemplateStrategy(BaseTemplateStrategy):
    def render_template(self, tpl, context):
        pass

    def render_string(self, html, context):
        pass


class AuthStrategy(BaseStrategy):
    DEFAULT_TEMPLATE_STRATEGY = AuthTemplateStrategy

    def __init__(self, session, request=None, tpl=None):
        self.request = request
        self.session = session

    def request_data(self, merge=True):
        if not self.request:
            return {}
        if merge:
            data = self.request[u'data']
        elif self.request.method == 'POST':
            data = self.request.POST
        else:
            data = self.request.GET
        return data

    def request_host(self):
        if self.request:
            return self.request['hosts']

    def session_get(self, name, default=None):
        return self.session.get(name, default)

    def session_set(self, name, value):
        self.session[name] = value
        if hasattr(self.session, 'modified'):
            self.session.modified = True

    def session_pop(self, name):
        return self.session.pop(name, None)

    def session_setdefault(self, name, value):
        return self.session.setdefault(name, value)

    def build_absolute_uri(self, path=None):
        if self.request:
            return self.request.build_absolute_uri(path)
        else:
            return path


