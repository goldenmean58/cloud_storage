#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : urls.py
# @Time     : Thu 12 Mar 2020 09:52:45 PM CST
# @Author   : Lishuxiang
# @E-mail   : lishuxiang@cug.edu.cn
# @Function : 

from django.conf.urls import url

from filemanager import path_end

import sys
from . import views

urlpatterns = (
    url(path_end, views.view, name='view'),
)
