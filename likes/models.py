from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class LikedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Generic relationship is made up of the three fields below
    # content type identifies the type of object in relationship
    # object_id provides the reference to that object
    # content_object so we can read the actual object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
