from django.contrib.auth.models import User
from django.test import TestCase

from django.urls import reverse

from catalogue.models import Categories,Modeles, Image_details
# Create your tests here.

#tester si la page index envoie bien un code 200
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        #recuperer l'url associer a la vue main
        response = self.client.get(reverse('home'))
        # verifier si le code de statut correspond a 200
        self.assertEqual(response.status_code, 200)

#verifier si la vue detail categorie envoi un code de status 200 si la categorie est trouvé
class DetailCategoriePageTestCase(TestCase):

    def setUp(self):
        # creer une nouvelle categorie
        test_cat = Categories.objects.create(nom_categorie="test_cate",image_categorie="./logo.jpeg")

        # recuperer la categorie creer
        self.test_categorie = Categories.objects.get(nom_categorie="test_cate")


    def test_detail_categorie_page(self):


        #recuperer la categorie creer
        test_cat_id  = self.test_categorie.id


        #on construit la requete vers la vue detail en passant en argument l'identifiant de la categorie
        response = self.client.get(reverse('catalogue:detail_categorie', args=(test_cat_id,)))

        #verifier que le code de statut de la reponse est 200
        self.assertEqual(response.status_code, 200)


    #verifier si un code 404 est envoyer
    def test_detail_categorie_page_returns_404(self):

        #recuperer la categorie creer
        test_cat_id = self.test_categorie.id + 1


        #on construit la requete vers la vue detail en passant en argument l'identifiant de la categorie
        response = self.client.get(reverse('catalogue:detail_categorie', args=(test_cat_id,)))

        #verifier que le code de statut de la reponse est 404
        self.assertEqual(response.status_code, 404)


#verifier si la vue detail categorie envoi un code de status 200 si la categorie est trouvé
class DetailModelePageTestCase(TestCase):
    def setUp(self):
        # creer une nouvelle categorie
        test_cat = Categories.objects.create(nom_categorie="test_cate",image_categorie="./logo.jpeg")

        # recuperer la categorie creer
        self.test_categorie = Categories.objects.get(nom_categorie="test_cate")

        # creer une nouvelle categorie
        test_mod = Modeles.objects.create(nom_modele="test_modele", categorie =test_cat ,image="./logo.jpeg")

        #recuperer la categorie creer
        self.test_modele  = Modeles.objects.get(nom_modele="test_modele")

    def test_detail_modele_page(self):
        test_mod_id = self.test_modele.id
        #on construit la requete vers la vue detail en passant en argument l'identifiant de la categorie
        response = self.client.get(reverse('catalogue:detail_modele', args=(test_mod_id,)))

        #verifier que le code de statut de la reponse est 200
        self.assertEqual(response.status_code, 200)


    def test_detail_modele_page_returns_404(self):
        test_mod_id = self.test_modele.id + 1


        #recuperer la categorie creer
        test_mod_id  = Modeles.objects.get(nom_modele="test_modele").id +1


        #on construit la requete vers la vue detail en passant en argument l'identifiant de la categorie
        response = self.client.get(reverse('catalogue:detail_modele', args=(test_mod_id,)))

        #verifier que le code de statut de la reponse est404
        self.assertEqual(response.status_code, 404)


