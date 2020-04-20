#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : urls.py
# @Time     : Thu 12 Mar 2020 09:52:45 PM CST
# @Author   : Lishuxiang
# @E-mail   : lishuxiang@cug.edu.cn
# @Function : 

from django.urls import path

from . import views

urlpatterns = (
    path("upload", views.upload_view, name='upload_view'),
    path("download/<link>/", views.download_view, name='download_view'),
    path("get_download", views.get_download_view, name='get_download_view'),
    path("view", views.view_view, name='view_view'),
    path("move", views.move_view, name='move_view'),
    path("copy", views.copy_view, name='copy_view'),
    path("delete", views.delete_view, name='delete_view'),
    path("share", views.share_view, name='share_view'),
    path("unshare", views.unshare_view, name='unshare_view'),
    path("create_dir", views.create_dir_view, name='create_dir_view'),
    path("restore", views.restore_view, name='restore_view'),
    path("get_total_size", views.get_total_size_view, name='get_total_size_view'),
    path("get_used_size", views.get_used_size_view, name='get_used_size_view'),
    path("get_space_size", views.get_space_size_view, name='get_space_size_view'),
)
