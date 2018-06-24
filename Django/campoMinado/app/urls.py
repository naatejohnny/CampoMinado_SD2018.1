from django.conf.urls import include, url
from django.urls import path
from . import views

urlpatterns = [
    url(r'iniciar/$', views.iniciar),
    url(r'jogada', views.jogada),
    url(r'main', views.main),
    path('', views.iniciar, name='iniciar'),
]