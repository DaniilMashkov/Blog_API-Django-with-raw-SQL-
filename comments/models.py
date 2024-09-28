from django.db import models
from django.utils.translation import gettext as _


class Comment(models.Model):
    author = models.CharField(_('author'), max_length=80)
    body = models.TextField(_('comment content'))
    created = models.DateTimeField(_('created at'), auto_now_add=True)
    post = models.ForeignKey(
        'posts.Post', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.body

    class Meta:
        db_table = 'comment'
