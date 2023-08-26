from django.urls import re_path # importer les urls du projet

from . import views

app_name = 'catalogue' # important pour le namespace



urlpatterns = [

    re_path(r'^$', views.main, name="home"),

    #re_path(r'^fav/(?P<id>[0-9]+)/$', views.favourite_add, name='favourite_add'),
    #re_path(r'^catalogue/favoris/$', views.favourite_list, name='favourite_list'),
    re_path(r'^catalogue/search-modele/$', views.search_modele, name="search-modele"),
    re_path(r'^catalogue/search-categorie/$', views.search_categorie, name="search-categorie"),
    re_path(r'^catalogue/categorie/modele/(?P<detail_modele_id>[0-9]+)/$', views.detail_modele, name="detail_modele"), #pb d'url


    re_path(r'^catalogue/categorie/(?P<detail_categorie_id>[0-9]+)/$', views.detail_categorie, name="detail_categorie"),    #pb d'url

    re_path(r'^about/$', views.aboutpage, name="about"),
    re_path(r'^catalogue/$', views.categoriepage, name="home-catalogue"),


]