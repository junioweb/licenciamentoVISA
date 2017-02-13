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


    url(r'^$', views.home, name='home'),
"""
from django.conf.urls import patterns, url, include
from django.contrib import admin
from segCadastro import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url('^accounts/login/', auth_views.login, name='login'),
    url('^accounts/logout/', auth_views.logout_then_login, {'login_url': 'login'}, name='logout'),
    url('^accounts/password_change/', auth_views.password_change, {'post_change_redirect': 'home'}, name='password_change'),
    url('^accounts/password_change/done/', auth_views.password_change_done, name='password_change_done'),
    url('^accounts/password_reset/', auth_views.password_reset, name='password_reset'),
    url('^accounts/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url('^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url('^accounts/reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
    url('^accounts/create/user/', views.cadastrar_user, name='cadastrar_user'),

    url(r'^admin/', admin.site.urls),
    url(r'^$', views.manutencao, name='manutencao'),
    """
    url(r'^example/', views.example, name='example'),
    url(r'^cadastro/processo/', views.processo_create, name='processo_create'),
    url(r'^cadastro/veiculo/', views.veiculo_create, name='veiculo_create'),
    url(r'^cadastro/responsavel/', views.responsavel_create, name='responsavel_create'),
    url(r'^cadastro/estabelecimento/pessoa_fisica/', views.p_fisica_create, name='p_fisica_create'),
    url(r'^cadastro/estabelecimento/pessoa_juridica/', views.p_juridica_create, name='p_juridica_create'),
    url(r'^documento/inclusao/', views.documento_include, name='documento_include'),
    url(r'^processo/listar/', views.processo_listar, name='processo_listar'),
    url(r'^responsavel/listar/', views.responsavel_listar, name='responsavel_listar'),
    url(r'^estabelecimento/pessoa_fisica/listar/', views.p_fisica_listar, name='p_fisica_listar'),
    url(r'^estabelecimento/pessoa_juridica/listar/', views.p_juridica_listar, name='p_juridica_listar'),
    url(r'^estabelecimento/pessoa_fisica/(?P<pk>[0-9]+)/editar/', views.p_fisica_editar, name='p_fisica_editar'),
    url(r'^estabelecimento/pessoa_juridica/(?P<pk>[0-9]+)/editar/', views.p_juridica_editar, name='p_juridica_editar'),
    url(r'^consulta/detalhes/$', views.consulta_geral, name='consulta_geral'),
    url(r'^estabelecimento/atividade/vincular/', views.estab_atv_vincular, name='estab_atv_vincular'),
    url(r'^autocomplete/service/processo/$', views.busca_autocomplete_processo, name='busca_autocomplete_processo'),
    url(r'^autocomplete/service/estabelecimento/$', views.busca_autocomplete_estabelecimento, name='busca_autocomplete_estabelecimento'),
    url(r'^autocomplete/service/atividade/$', views.busca_autocomplete_atividade, name='busca_autocomplete_atividade'),
    url(r'^autocomplete/service/responsavel/$', views.busca_autocomplete_responsavel, name='busca_autocomplete_responsavel'),
    url(r'^processo/(?P<pk>[0-9]+)/imprimir', views.p_imprimir, name='p_imprimir'),
    url(r'^processo/reorientar/$', views.processo_reorientar, name='processo_reorientar'),
    url(r'^responsavel/(?P<pk>[0-9]+)/editar', views.responsavel_editar, name='responsavel_editar'),"""
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
