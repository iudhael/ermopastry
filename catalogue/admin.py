from django.contrib import admin
from .models import *
# Register your models here.

class Detail_modeleInline(admin.TabularInline):
    model = Image_details
    fieldsets = [
        (None, {'fields': ['img_detail', 'date_de_publication_detail_modele', ]})
    ]
    extra = 1

class ModeleInline(admin.TabularInline):
    model = Modeles

    fieldsets = [
        (None, {'fields': ['nom_modele',
                           #'description',
                           'date_de_publication',
                           'image',
                           #'favourites',
                           ]})
    ]
    extra = 1

@admin.register(Categories)
class CategorieAdmin(admin.ModelAdmin):
    inlines = [ModeleInline,]
    readonly_fields = ["created_at_categorie"]
    search_fields = ['nom_categorie','created_at_categorie', 'date_de_publication_categorie', "creat"]

@admin.register(Modeles)
class ModeleAdmin(admin.ModelAdmin):
    inlines = [Detail_modeleInline,]
    readonly_fields = ["created_at_modele"]
    search_fields = ['nom_modele', 'created_at_modele', 'date_de_publication', ]


#admin.site.register(Favories)