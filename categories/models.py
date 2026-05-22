from django.db import models
from django.utils import timezone


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Category(models.Model):
    title = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    delete_at = models.DateTimeField(null=True, blank=True)

    objects = CategoryManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.delete_at = timezone.now()
        self.save(update_fields=["is_deleted", "delete_at"])

    def __str__(self):
        return self.title