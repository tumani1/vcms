# coding: utf-8

from flask.ext.admin.form import upload


class ImageUploadInput(upload.ImageUploadInput):

    def get_url(self, field):
        return "http://cdn.serialov.tv/s/upload/media/{0}".format(field.data)