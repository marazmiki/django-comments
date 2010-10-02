from django.db import models
from reusable.comments import models as comments_models

class ContentObject(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        app_label = 'comments'


#comments_models.ContentObject = ContentObject