from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os, shutil
# Create your models here.




class Categories(models.Model):
    # robe, chemisier, combinaison...
    nom_categorie = models.CharField('nom de la categorie', max_length=50, null=True, blank=True)
    created_at_categorie = models.DateTimeField('date creation de la categorie', auto_now_add=True)

    date_de_publication_categorie = models.DateField('date de publication de la categorie ', default="2022-11-10")
    image_categorie = models.ImageField('image de la categorie du modele', upload_to=f'categories/')


    class Meta:
        verbose_name = "categorie"

    def __str__(self):
        return self.nom_categorie

    def save(self, *args, **kwargs): # remplacer la methode de sauvegarde por ajouter des fonctionaliter au save parent
        super(Categories, self).save(*args, **kwargs)

        #chemin actuel de l'image
        chemin_actuel = str(self.image_categorie)
        #print(chemin_actuel)
        picture_name =  chemin_actuel.split('/')[-1]
        #print(picture_name)
        
        new_dossier = f'media/categories/{self.nom_categorie}'
        #print(new_dossier)
        #chemin par defaut de l'enregistrement de l'image 
        default_chemin =f'media/categories/{picture_name}'
        #print(default_chemin)
        #nouveau chemin de l'enregistrement de l'Image
        new_chemin =f'{new_dossier}/{picture_name}'
        #print(new_chemin)

        
        if not os.path.isdir(new_dossier):
            os.makedirs(new_dossier)

        
        if os.path.isfile(default_chemin):
            new_chemin_actuel = f'categories/{self.nom_categorie}/{picture_name}'
            shutil.move(default_chemin, new_chemin)
            self.image_categorie = new_chemin_actuel
            self.save()
        
        img = Image.open(self.image_categorie.path)  #on ouvre l'image acctuelle et on va redimentionner
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)   #redimentioner 300/300
            img.save(self.image_categorie.path)
    
        







class Modeles(models.Model): 

    nom_modele = models.CharField('nom modele', max_length=50, null=True, blank=True)
    created_at_modele = models.DateTimeField('date creation du modele', auto_now_add=True)


    #description = models.TextField('description du modele', blank=True)

    date_de_publication = models.DateField('date de publication du modele ', default="2022-11-10")

    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE)

    image = models.ImageField('image du modele', upload_to='categories/') #enregistrer l'image dans le dossier de la categorie selectioner

    #favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)


    class Meta:
        verbose_name = "modele"

    def __str__(self):
        if self.nom_modele != '':
            return self.nom_modele + f' ({self.categorie.nom_categorie})'
        else:
            return f'{self.pk} ({self.categorie.nom_categorie})'

    def save(self, *args, **kwargs): # remplacer la methode de sauvegarde por ajouter des fonctionaliter au save parent
        super(Modeles, self).save(*args, **kwargs)

        #chemin actuel de l'image
        chemin_actuel = str(self.image)
        #print(chemin_actuel)
        picture_name =  chemin_actuel.split('/')[-1]
        #print(picture_name)

        #si le modele a un titre
        if self.nom_modele != '':
            new_dossier = f'media/categories/{self.categorie.nom_categorie}/modele_{self.nom_modele}'
        else:
            new_dossier = f'media/categories/{self.categorie.nom_categorie}/modele_{self.pk}'

        #print(new_dossier)
        #chemin par defaut de l'enregistrement de l'image 
        default_chemin =f'media/categories/{picture_name}'
        #print(default_chemin)
        #nouveau chemin de l'enregistrement de l'Image
        new_chemin =f'{new_dossier}/{picture_name}'
        #print(new_chemin)

        
        if not os.path.isdir(new_dossier):
            os.makedirs(new_dossier)

        
        if os.path.isfile(default_chemin):
            if self.nom_modele != '':
                new_chemin_actuel = f'categories/{self.categorie.nom_categorie}/modele_{self.nom_modele}/{picture_name}'
            else:
                new_chemin_actuel = f'categories/{self.categorie.nom_categorie}/modele_{self.pk}/{picture_name}'
                
            shutil.move(default_chemin, new_chemin)
            self.image = new_chemin_actuel
            self.save()
        
        
        img = Image.open(self.image.path)  #on ouvre l'image acctuelle et on va redimentionner
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)   #redimentioner 300/300
            img.save(self.image.path)
        
    


class Image_details(models.Model): 
    img_detail = models.ImageField('image de profile du modele', upload_to='categories/')
    created_at_detail_modele = models.DateTimeField('date creation de la detail du modele', auto_now_add=True)

    date_de_publication_detail_modele = models.DateField('date de publication du de la detail du modele ', default="2022-11-10")


    img_detail_modele = models.ForeignKey(Modeles, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "image detail du modele"

    def __str__(self):
        return f'{self.img_detail_modele.nom_modele} detail'

    def save(self, *args, **kwargs): # remplacer la methode de sauvegarde por ajouter des fonctionaliter au save parent
        super(Image_details, self).save(*args, **kwargs)

        #chemin actuel de l'image
        chemin_actuel = str(self.img_detail)
        #print(chemin_actuel)
        picture_name =  chemin_actuel.split('/')[-1]
        #print(picture_name)

        #si le modele a un titre
        if self.img_detail_modele.nom_modele != '':
            new_dossier = f'media/categories/{self.img_detail_modele.categorie.nom_categorie}/modele_{self.img_detail_modele.nom_modele}'
            #print(new_dossier)
        else:
            new_dossier = f'media/categories/{self.img_detail_modele.categorie.nom_categorie}/modele_{self.img_detail_modele.pk}'

        
        #chemin par defaut de l'enregistrement de l'image 
        default_chemin =f'media/categories/{picture_name}'
        #print(default_chemin)
        #nouveau chemin de l'enregistrement de l'Image
        new_chemin =f'{new_dossier}/{picture_name}'
        #print(new_chemin)

        
        if not os.path.isdir(new_dossier):
            os.makedirs(new_dossier)

        
        if os.path.isfile(default_chemin):
            if self.img_detail_modele.nom_modele != '':
                new_chemin_actuel = f'categories/{self.img_detail_modele.categorie.nom_categorie}/modele_{self.img_detail_modele.nom_modele}/{picture_name}'
            else:
                new_chemin_actuel = f'categories/{self.img_detail_modele.categorie.nom_categorie}/modele_{self.img_detail_modele.pk}/{picture_name}'

            shutil.move(default_chemin, new_chemin)
            self.img_detail = new_chemin_actuel
            self.save()
        
        
        img = Image.open(self.img_detail.path)  #on ouvre l'image acctuelle et on va redimentionner
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)   #redimentioner 300/300
            img.save(self.img_detail.path)

"""
class Favories(models.Model): 
    user_fav = models.ForeignKey(User, on_delete=models.CASCADE)
    modele_fav = models.ForeignKey(Modeles, on_delete=models.CASCADE)
    value_fav = models.BooleanField('value_fav', default=False)

    class Meta:
        verbose_name = "favorie"

    def __str__(self):
        return str(self.modele_fav)
"""
