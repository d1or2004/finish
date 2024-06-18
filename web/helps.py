import uuid
from django.db.models import TextChoices


class SaveModelFields(object):
    @staticmethod
    def product_image_path(instance, filename):
        image_extension = filename.split('.')[-1]
        return f"media/product/{uuid.uuid4()}.{image_extension}"
