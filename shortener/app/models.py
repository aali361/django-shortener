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

