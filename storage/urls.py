#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : urls.py
# @Time     : Thu 12 Mar 2020 09:52:45 PM CST
# @Author   : Lishuxiang
# @E-mail   : lishuxiang@cug.edu.cn
# @Function : 

from django.conf.urls import url

from . import views

urlpatterns = (
    url("upload", views.upload_view, name='upload_view'),
    url("download", views.download_view, name='download_view'),
    url("view", views.view_view, name='view_view'),
    url("move", views.move_view, name='move_view'),
    url("copy", views.copy_view, name='copy_view'),
    url("delete", views.delete_view, name='delete_view'),
    url("share", views.share_view, name='share_view'),
    url("unshare", views.unshare_view, name='unshare_view'),
    url("create_dir", views.create_dir_view, name='create_dir_view'),
)
