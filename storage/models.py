from django.db import models

# Create your models here.

class Dir(models.Model):
    id = models.AutoField(primary_key=True)
    dir_name = models.CharField(max_length=256)
    user_name = models.CharField(max_length=256)
    parent_id = models.IntegerField()

class File(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=256)
    file_size = models.BigIntegerField()
    user_name = models.CharField(max_length=256)
    md5 = models.CharField(max_length=32)
    blake2 = models.CharField(max_length=32)
    parent_id = models.CharField(max_length=1024)
    is_shared = models.BooleanField()
    shared_key = models.CharField(max_length=4, blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)


class DownloadLink(models.Model):
    md5 = models.CharField(max_length=32)
    blake2 = models.CharField(max_length=32)
    link = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now=True)
    invalid_time = models.DateTimeField()

