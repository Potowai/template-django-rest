from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Product

class ProductApiCrudTests(APITestCase):
    """
    Suite de tests pour le CRUD complet du ViewSet Product.
    """

    @classmethod
    def setUpClass(cls):
        """
        Exécuté une seule fois pour la classe de test.
        Permet de définir les URLs qui ne changent pas.
        """
        super().setUpClass()
        cls.list_create_url = reverse('product-list')

    def setUp(self):
        """
        Exécuté avant chaque méthode de test.
        Met en place un environnement propre pour chaque test.
        """
        # --- Utilisateur et authentification ---
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        
        # Générer un token JWT pour cet utilisateur
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Authentifier le client de test
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # --- Données de test ---
        self.product1 = Product.objects.create(name='Laptop Pro', description='A powerful laptop', price=1500.00)
        self.product2 = Product.objects.create(name='Wireless Mouse', description='A comfy mouse', price=50.00)
        
        # URL pour les actions de détail (retrieve, update, delete)
        self.detail_url = reverse('product-detail', kwargs={'pk': self.product1.pk})

    def test_list_products_authenticated(self):
        """
        Vérifie que les utilisateurs authentifiés peuvent lister les produits.
        [GET] /api/products/
        """
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Vérifie que les 2 produits créés sont bien dans la réponse
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.product2.name) # Ordered by -created_at

    def test_retrieve_product_authenticated(self):
        """
        Vérifie qu'un utilisateur authentifié peut récupérer un produit spécifique.
        [GET] /api/products/{pk}/
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product1.name)

    def test_create_product_authenticated(self):
        """
        Vérifie qu'un utilisateur authentifié peut créer un produit.
        [POST] /api/products/
        """
        initial_product_count = Product.objects.count()
        product_data = {'name': 'New Keyboard', 'description': 'A mechanical keyboard', 'price': '120.50'}
        
        response = self.client.post(self.list_create_url, product_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), initial_product_count + 1)
        self.assertEqual(response.data['name'], 'New Keyboard')

    def test_update_product_authenticated(self):
        """
        Vérifie qu'un utilisateur authentifié peut mettre à jour un produit (PUT).
        [PUT] /api/products/{pk}/
        """
        update_data = {'name': 'Laptop Pro X', 'description': 'An even more powerful laptop', 'price': '1750.00'}
        
        response = self.client.put(self.detail_url, update_data, format='json')
        self.product1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.product1.name, 'Laptop Pro X')
        self.assertEqual(self.product1.price, 1750.00)

    def test_partial_update_product_authenticated(self):
        """
        Vérifie qu'un utilisateur authentifié peut mettre à jour partiellement un produit (PATCH).
        [PATCH] /api/products/{pk}/
        """
        patch_data = {'price': '1600.50'}
        
        response = self.client.patch(self.detail_url, patch_data, format='json')
        self.product1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.product1.price, 1600.50)
        self.assertEqual(self.product1.name, 'Laptop Pro') # Le nom n'a pas changé

    def test_delete_product_authenticated(self):
        """
        Vérifie qu'un utilisateur authentifié peut supprimer un produit.
        [DELETE] /api/products/{pk}/
        """
        initial_product_count = Product.objects.count()
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), initial_product_count - 1)

class ProductApiSecurityTests(APITestCase):
    """
    Suite de tests dédiée à la sécurité des endpoints Product.
    Vérifie que les utilisateurs non authentifiés ne peuvent pas y accéder.
    """

    def setUp(self):
        """
        Crée des données de test mais n'authentifie PAS le client.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.product = Product.objects.create(name='Test Product', price=100)
        self.list_url = reverse('product-list')
        self.detail_url = reverse('product-detail', kwargs={'pk': self.product.pk})

    def test_unauthenticated_access_fails(self):
        """
        Vérifie que l'accès non authentifié à tous les endpoints du CRUD échoue avec une erreur 401.
        """
        # Test List
        response_get = self.client.get(self.list_url)
        self.assertEqual(response_get.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test Retrieve
        response_retrieve = self.client.get(self.detail_url)
        self.assertEqual(response_retrieve.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test Create
        response_post = self.client.post(self.list_url, {'name': 'New', 'price': '10'}, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test Update
        response_put = self.client.put(self.detail_url, {'name': 'Update', 'price': '20'}, format='json')
        self.assertEqual(response_put.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test Delete
        response_delete = self.client.delete(self.detail_url)
        self.assertEqual(response_delete.status_code, status.HTTP_401_UNAUTHORIZED)