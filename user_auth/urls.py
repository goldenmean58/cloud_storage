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
    url("login", views.login_view, name='login_view'),
    url("register", views.register_view, name='register_view'),
    url("logout", views.logout_view, name='logout_view'),
)
