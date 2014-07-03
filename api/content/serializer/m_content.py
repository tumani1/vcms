# coding=utf-8
from models.content import Content


class mContentSerializer(object):

    def __init__(self, content):
        """
        В content нужно подавать либо экземпляр модели, либо список экземпляров.
        content проверяется на то, что он - модель/ли Content.
        """
        if content is None:
            raise TypeError("attr must be Content instance")

        self.content = content
        self.is_list = isinstance(content, list)

        if self.is_list:
            are_content = (isinstance(c, Content) for c in content)
            if not all(are_content):
                raise TypeError("list has obj is not Content instance")
        else:
            if not isinstance(content, Content):
                raise TypeError("content is not Content instance")

    def get_data(self):
        if self.is_list:
            return [dict(id=c.id, title=c.title, text=c.text) for c in self.content]
        else:
            return dict(id=self.content.id, title=self.content.title, text=self.content.text)