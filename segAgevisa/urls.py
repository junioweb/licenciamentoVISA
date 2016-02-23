# -*- encoding: utf-8 -*-

"""segAgevisa URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from segCadastro import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^example/', views.example, name='example'),
    url(r'^cadastro/processo/', views.processo_create, name='processo_create'),
    url(r'^cadastro/responsavel/', views.responsavel_create, name='responsavel_create'),
    url(r'^cadastro/estabelecimento/pessoa_fisica/', views.p_fisica_create, name='p_fisica_create'),
    url(r'^cadastro/estabelecimento/pessoa_juridica/', views.p_juridica_create, name='p_juridica_create'),
    url(r'^processo/listar/', views.processo_listar, name='processo_listar'),
    url(r'^responsavel/listar/', views.responsavel_listar, name='responsavel_listar'),
    url(r'^estabelecimento/pessoa_fisica/listar/', views.p_fisica_listar, name='p_fisica_listar'),
    url(r'^estabelecimento/pessoa_juridica/listar/', views.p_juridica_listar, name='p_juridica_listar'),
    url(r'^estabelecimento/pessoa_fisica/(?P<pk>[0-9]+)/editar/', views.p_fisica_editar, name='p_fisica_editar'),
    url(r'^estabelecimento/pessoa_juridica/(?P<pk>[0-9]+)/editar/', views.p_juridica_editar, name='p_juridica_editar'),
    url(r'^estabelecimento/atividade/vincular/', views.estab_atv_vincular, name='estab_atv_vincular'),
    url(r'^processo/(?P<pk>[0-9]+)/imprimir', views.p_imprimir, name='p_imprimir'),
    url(r'^processo/(?P<pk>[0-9]+)/tramitar', views.processo_tramitar, name='processo_tramitar'),
    url(r'^responsavel/(?P<pk>[0-9]+)/editar', views.responsavel_editar, name='responsavel_editar'),
    # url(r'^cadastro/estabelecimento/', views.estabelecimento, name='estabelecimento'),
]
