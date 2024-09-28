from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

User = get_user_model()


def get_upload_path(instance, filename):
    return f'posts/{instance.id}/{filename}'


class Post(models.Model):
    title = models.CharField(_('title'), max_length=120)
    description = models.CharField(_('description'), max_length=120)
    text = models.TextField(_('text'))
    image = models.ImageField(
        _('image'), upload_to=get_upload_path, blank=True, null=True)
    created = models.DateTimeField(_('created_at'), auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'post'
