# coding: utf-8

from flask.ext.admin.form import upload
from werkzeug.datastructures import FileStorage

from admin.widgets import ImageUploadInput


class ImageUploadField(upload.ImageUploadField):
    widget = ImageUploadInput()

    def populate_obj(self, obj, name):
        field = getattr(obj, name, None)
        if field:
            # If field should be deleted, clean it up
            if self._should_delete:
                self._delete_file(field)
                setattr(obj, name, None)
                return

        if self.data and self.data.filename and isinstance(self.data, FileStorage):
            if field:
                self._delete_file(field)

            filename = self.generate_name(obj, self.data)
            self.data.filename = filename
            setattr(obj, name, filename)