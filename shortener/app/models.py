from django.db import models

from user import models as usr_models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class URL(BaseModel):
    url = models.URLField()
    short = models.URLField(unique=True)
    owner = models.ForeignKey(usr_models.Profile, on_delete=models.CASCADE, related_name='urls',
                                related_query_name='url')

    def __str__(self):
        return self.url

class Report(BaseModel):
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='reports', related_query_name='report')
    viewer = models.ForeignKey(usr_models.Profile, on_delete=models.CASCADE, related_name='reports', related_query_name='report')

    MOBILE = 'mobile'
    DESKTOP = 'desktop'
    device_types = ((MOBILE, 'موبایل'), (DESKTOP, 'دسکتاپ'),)
    device = models.CharField(max_length=10, choices=device_types, default='NA')

    browser = models.CharField(max_length=50, default='NA')

    def __str__(self):
        return self.url

