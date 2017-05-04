from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import random
import string


class ApiKeys(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    key = models.CharField(max_length=32, verbose_name=_('key'))

    def save(self, *args, **kwargs):
        if not self.id:
            self.key = ''\
                .join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        super(ApiKeys, self).save(*args, **kwargs)
