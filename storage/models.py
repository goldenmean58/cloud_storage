from django.db import models

# Create your models here.

class File(models.Model):
    id = models.AutoField(primary_key=True)
    is_dir = models.BooleanField()
    dir_name = models.CharField(max_length=65535, null=True, blank=True)
    file_name = models.CharField(max_length=256)
    file_size = models.BigIntegerField(null=True, blank=True)
    user_name = models.CharField(max_length=256)
    md5 = models.CharField(max_length=32, null=True, blank=True)
    blake2 = models.CharField(max_length=32, null=True, blank=True)
    parent_id = models.IntegerField()
    is_shared = models.BooleanField()
    shared_key = models.CharField(max_length=4, blank=True, null=True)
    shared_expire_time = models.DateTimeField(auto_now_add=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    last_dir_name = models.CharField(max_length=65535, null=True, blank=True)


class DownloadLink(models.Model):
    md5 = models.CharField(max_length=32)
    blake2 = models.CharField(max_length=32)
    link = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now=True)
    file_name = models.CharField(max_length=256)

class RawFile(models.Model):
    md5 = models.CharField(max_length=32)
    blake2 = models.CharField(max_length=32)
    count = models.IntegerField()
