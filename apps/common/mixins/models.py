# -*- coding: utf-8 -*-
#

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

__all__ = [
    "NoDeleteManager", "NoDeleteModelMixin", "NoDeleteQuerySet",
]


class NoDeleteQuerySet(models.query.QuerySet):

    def delete(self):
        return self.update(is_discard=True, discard_time=timezone.now())


class NoDeleteManager(models.Manager):

    def get_all(self):
        return NoDeleteQuerySet(self.model, using=self._db)

    def get_queryset(self):
        return NoDeleteQuerySet(self.model, using=self._db).filter(is_discard=False)

    def get_deleted(self):
        return NoDeleteQuerySet(self.model, using=self._db).filter(is_discard=True)


class NoDeleteModelMixin(models.Model):
    is_discard = models.BooleanField(verbose_name=_("is discard"), default=False)
    discard_time = models.DateTimeField(verbose_name=_("discard time"), null=True, blank=True)

    objects = NoDeleteManager()

    class Meta:
        abstract = True

    def delete(self):
        self.is_discard = True
        self.discard_time = timezone.now()
        return self.save()


class DebugQueryManager(models.Manager):
    def get_queryset(self):
        import traceback
        lines = traceback.format_stack()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        for line in lines[-10:-1]:
            print(line)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        queryset = super().get_queryset()
        return queryset
