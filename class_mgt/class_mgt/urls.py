"""class_mgt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin

import main.views.auth as auth
import main.views.event as e
import main.views.profile as p

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^add_event$', e.add_event, name='add_event'),
    url(r'^event_list$', e.event_list, name='event_list'),
    url(r'^event_details$', e.event_details, name='event_details'),
    url(r'^event_record$', e.event_record, name='event_record'),
    url(r'^join_event$', e.join_event, name='join_event'),
    url(r'^remove_event$', e.remove_event, name='remove_event'),
    url(r'^quit_event$', e.quit_event, name='quit_event'),
    url(r'^profile$', p.profile, name='profile'),
    url(r'^login$', auth.login_page, name='login'),
    url(r'^logout$', auth.logout_page, name='logout'),
    url(r'^register$', auth.register, name='register'),
    url(r'^password_reset$', auth.password_reset, name='password_reset'),
    url(r'^password_reset/done$', auth.password_reset_done, name='password_reset_done',),
    url(r'^', auth.login_page),
]
