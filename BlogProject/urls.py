"""BlogProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.post_list_view),
    url(r'^tag/(?P<tag_slug>[-_\w]+)/$',views.post_list_view,name='post_list_by_tag_name'),
    url(r'^(?P<year>\d{4})/(?P<post>[-_\w]+)/$', views.post_detail_view, name='post_detail'),
    url(r'^(?P<id>\d+)/share/$', views.mail_send_view)
]
