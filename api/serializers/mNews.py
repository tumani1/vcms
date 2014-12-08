from utils.serializer import DefaultSerializer

__all__ = ['mNews']


class mNews(DefaultSerializer):

    __read_fields = {
        'id': '',
        'text': '',
        'published': '',
        'object': '',
        'comments_cnt': '',
    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields
        super(mNews, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_text(self, instance, **kwargs):
        return instance.text

    def transform_published(self, instance, **kwargs):
        return instance.published

    def transform_comments_cnt(self, instance, **kwargs):
        return instance.comments_cnt