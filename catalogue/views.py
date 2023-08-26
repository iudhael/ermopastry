from django.shortcuts import render,  get_object_or_404, redirect
from django.http import HttpResponse ,HttpResponseRedirect
from .models import * 
import datetime
import random
from datetime import date
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.contrib.auth.decorators import login_required
# Create your views here.

global today_date

today_date = date.today()
"""
def index(request):
    context = {


    }

    return render(request, 'catalogue/listing_categorie.html', context)
"""

def main(request):

    categories = Categories.objects.filter(date_de_publication_categorie__lt=today_date).order_by('nom_categorie')
    categorie_objs = list(categories)



    random.shuffle(categorie_objs)
    categorie_objs = categorie_objs[:3]
    
    #print(categorie_objs)
    navbar = "home"
    context = {
        'categorie_objs': categorie_objs,
        "navbar": navbar,
            }

    return render(request, 'catalogue/home.html', context)


def aboutpage(request):
    navbar = "about"
    context = {
        'navbar' : navbar
    }
    return render(request, 'catalogue/about.html', context)

"""
@login_required(login_url='authentification:login')
def favourite_list(request):
    new = Modeles.objects.filter(favourites=request.user)
    navbar = "favori"
    context = {
        'new' : new,
        'navbar': navbar,
    }

    return render(request, 'catalogue/favoris.html', context)



@login_required(login_url='authentification:login')
def favourite_add(request, id):
    modele = get_object_or_404(Modeles, pk=id)
    if modele.favourites.filter(id=request.user.id).exists():
        modele.favourites.remove(request.user)
    else:
        modele.favourites.add(request.user)

    favorie, created = Favories.objects.get_or_create(user_fav=request.user, modele_fav_id=id)
    if not created:
        if favorie.value_fav == False:
            favorie.value_fav = True
        else:
            favorie.value_fav = False
    favorie.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
"""



def categoriepage(request):
    categories_list = Categories.objects.filter(date_de_publication_categorie__lt=today_date).order_by('-id')
    paginator = Paginator(categories_list, 6)
    if request.method == 'POST':
            page = request.POST.get('page')
            #print(page)
    else:
        page = request.GET.get('page')
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        #si la page n'est pas un entier delivrer la premier page
        categories = paginator.page(1)
    except EmptyPage:
        # si le num de page est en dehors de la list delivrer les items correpondant à la derniere page
        categories = paginator.page(paginator.num_pages)

    #print(categories)
    navbar = "catalogue"
    context = {
        'categories':categories,
        'paginate': True,
        "navbar" : navbar,
            }
    return render(request, 'catalogue/listing_categorie.html', context)


def detail_categorie(request, detail_categorie_id):
    global categorie_name

    #print(detail_categorie_id)
    categorie_name = get_object_or_404(Categories, pk=detail_categorie_id)
    
    #print(categorie_name)



    #print(today_date)
    modele_categories_list = Modeles.objects.filter(categorie=categorie_name, date_de_publication__lt=today_date).order_by('-id')
    paginator = Paginator(modele_categories_list, 4)

    if request.method == 'POST':
            page = request.POST.get('page')
            #print(page)
    else:
        page = request.GET.get('page')
    try:
        modele_categories = paginator.page(page)
    except PageNotAnInteger:
        #si la page n'est pas un entier delivrer la premier page
        modele_categories = paginator.page(1)
    except EmptyPage:
        # si le num de page est en dehors de la list delivrer les items correpondant à la derniere page
        modele_categories = paginator.page(paginator.num_pages)
    #print(modele_categories)
    navbar = "catalogue"
    context = {
        'modele_categories':modele_categories,
        'categorie_name':categorie_name,
        'paginate': True,
        "navbar" : navbar,

              
        }
    return render(request, 'catalogue/listing_modele.html', context)



def detail_modele(request, detail_modele_id):
    modele_name = get_object_or_404(Modeles, pk=detail_modele_id)
    #print(modele_name)
    modeles = Image_details.objects.filter(img_detail_modele=modele_name, date_de_publication_detail_modele__lt=today_date).order_by('-id')

    #print(modeles)
    paginator = Paginator(modeles, 5)

    if request.method == 'POST':
        page = request.POST.get('page')
        # print(page)
    else:
        page = request.GET.get('page')
    try:
        details_modeles = paginator.page(page)
    except PageNotAnInteger:
        # si la page n'est pas un entier delivrer la premier page
        details_modeles = paginator.page(1)
    except EmptyPage:
        # si le num de page est en dehors de la list delivrer les items correpondant à la derniere page
        details_modeles = paginator.page(paginator.num_pages)


    #print(modeles)
    navbar = "catalogue"
    context = {
        'details_modeles': details_modeles,
        'paginate': True,
        'modele_name': modele_name,
        "navbar": navbar,
        }
    return render(request, 'catalogue/detail_modele.html', context)




def search_categorie(request):

    query = request.GET.get('query') # avec GET tous ce qui est taper dans l'url comme recherche est capturer
    query = query.lower()
    if not query:
        categories = Categories.objects.filter(date_de_publication_categorie__lt=today_date).order_by('nom_categorie')
        #print(categories)
    else:
        # title__icontains contient la requette qui est le titre mais pas exactement le titre de l'album si le titre est mal taper ou imcomplet
        categories = Categories.objects.filter(date_de_publication_categorie__lt=today_date, nom_categorie__icontains=query).order_by('nom_categorie')
        #print(categories)

        if not categories.exists():
            categories = Categories.objects.filter(date_de_publication_categorie__lt=today_date, nom_categorie__icontains=query).order_by('nom_categorie') # chercher dans la table  les noms qui correspondent aux requette et renvoyer des album
            #print(categories)



    title = "Résultats pour la requête %s"%query
    context = {
        'categories': categories,
        'title': title
    }

    return render(request, 'catalogue/search_categorie.html', context)


def search_modele(request):
    #categorie_id = get_object_or_404(Categories, pk=detail_categorie_id)
    
    query = request.GET.get('query') # avec GET tous ce qui est taper dans l'url comme recherche est capturer

    query = query.lower()
    if not query:
        modele_categories = Modeles.objects.filter(categorie=categorie_name, date_de_publication__lt=today_date).order_by('nom_modele')
        #print(modele_categories)
    else:
        # title__icontains contient la requette qui est le titre mais pas exactement le titre de l'album si le titre est mal taper ou imcomplet
        modele_categories = Modeles.objects.filter(categorie=categorie_name, date_de_publication__lt=today_date, nom_modele__icontains=query).order_by('nom_modele')
        #print(modele_categories)

        if not modele_categories.exists():
            modele_categories = Modeles.objects.filter(categorie=categorie_name, date_de_publication__lt=today_date, nom_modele__icontains=query).order_by('nom_modele') # chercher dans la table  les noms qui correspondent aux requette et renvoyer des album
            #print(modele_categories)



    title = "Résultats pour la requête %s"%query
    context = {
        'modele_categories': modele_categories,
        'title': title
    }

    return render(request, 'catalogue/search_modele.html', context)