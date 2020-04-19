from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_name = models.CharField(max_length=256)
    total_size = models.BigIntegerField(null=True, blank=True)
    used_size = models.BigIntegerField(null=True, blank=True)
