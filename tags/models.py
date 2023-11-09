from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.

class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        # find tags for a given product
        content_type = ContentType.objects.get_for_model(obj_type)
        # content_type is now a row from the ContentType table. Specifically the row that represents the Product model
        queryset = TaggedItem.objects. \
            select_related('tag') \
            .filter(content_type=content_type,object_id=obj_id)
        
        return queryset

class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Generic relationship is made up of the three fields below
    # content type identifies the type of object in relationship
    # object_id provides the reference to that object
    # content_object so we can read the actual object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
