from django.db import models
from django.utils import timezone

from user import models as usr_models

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class URL(BaseModel):
    url = models.URLField()
    short = models.URLField(unique=True)
    owner = models.ForeignKey(usr_models.Profile, on_delete=models.CASCADE, related_name='urls',
                                related_query_name='url')

    def __str__(self):
        return self.url

class Access(BaseModel):
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='accesses', related_query_name='access')
    viewer = models.ForeignKey(usr_models.Profile, on_delete=models.CASCADE, related_name='accesses', related_query_name='access')

    MOBILE = 'mobile'
    DESKTOP = 'desktop'
    device_types = ((MOBILE, 'موبایل'), (DESKTOP, 'دسکتاپ'),)
    device = models.CharField(max_length=10, choices=device_types, default='NA')

    browser = models.CharField(max_length=50, default='NA')

    def __str__(self):
        return str(self.url)


class Report(BaseModel):
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='reports', related_query_name='report')

    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    time_types = ((DAY, 'روز'), (WEEK, 'هفته'), (MONTH, 'ماه'))
    type = models.CharField(max_length=10, choices=time_types, default='NA')

    view = models.IntegerField(default=0)
    device = models.JSONField(null=True)
    browser = models.JSONField(null=True)
    user_repetitive = models.BooleanField(default=False)
