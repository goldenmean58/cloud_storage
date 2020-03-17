# Generated by Django 3.0.4 on 2020-03-17 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md5', models.CharField(max_length=32)),
                ('blake2', models.CharField(max_length=32)),
                ('link', models.CharField(max_length=256)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('file_name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_dir', models.BooleanField()),
                ('dir_name', models.CharField(blank=True, max_length=256, null=True)),
                ('file_name', models.CharField(max_length=256)),
                ('file_size', models.BigIntegerField(blank=True, null=True)),
                ('user_name', models.CharField(max_length=256)),
                ('md5', models.CharField(blank=True, max_length=32, null=True)),
                ('blake2', models.CharField(blank=True, max_length=32, null=True)),
                ('parent_id', models.CharField(max_length=1024)),
                ('is_shared', models.BooleanField()),
                ('shared_key', models.CharField(blank=True, max_length=4, null=True)),
                ('shared_expire_time', models.DateTimeField(auto_now_add=True)),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RawFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md5', models.CharField(max_length=32)),
                ('blake2', models.CharField(max_length=32)),
                ('count', models.IntegerField()),
            ],
        ),
    ]
