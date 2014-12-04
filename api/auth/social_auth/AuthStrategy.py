from social.strategies.base import BaseStrategy, BaseTemplateStrategy

TEST_URI = 'http://nexttv.com'


class AuthTemplateStrategy(BaseTemplateStrategy):
    def render_template(self, tpl, context):
        return tpl

    def render_string(self, html, context):
        return html


class AuthStrategy(BaseStrategy):
    DEFAULT_TEMPLATE_STRATEGY = AuthTemplateStrategy

    def __init__(self, storage, session, backends, backend, request=None, tpl=None):
        self.backend = backend(strategy=self)
        self.backends = backends
        self.request = request
        self.session = session
        self.storage = storage

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

    def start(self):
        if self.backend.uses_redirect():
            return self.redirect(self.backend.auth_url())
        else:
            return self.html(self.backend.auth_html())

    def request_host(self):
        if self.request:
            return self.request['hosts']

    def session_get(self, name, default=None):
        return u'/tokenize/?back_utl=/'

    def session_set(self, name, value):
        self.session[name] = value
        if hasattr(self.session, 'modified'):
            self.session.modified = True

    def session_pop(self, name):
        return self.session.pop(name, None)

    def session_setdefault(self, name, value):
        return self.session.setdefault(name, value)

    def build_absolute_uri(self, path=None):
        path = path or ''
        if path.startswith('http://') or path.startswith('https://'):
            return path
        return TEST_URI + path


