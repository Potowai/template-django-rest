from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializers import UserSerializer, ProductSerializer

class SignupView(generics.CreateAPIView):
    """
    Vue pour l'inscription d'un nouvel utilisateur.
    Elle est publique (AllowAny).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # La permission est explicitement définie sur `AllowAny` pour outrepasser
    # le paramètre global `IsAuthenticated`.
    permission_classes = [AllowAny]

class HealthCheckView(APIView):
    """
    Vue simple pour vérifier que l'API est en ligne.
    Elle est publique (AllowAny).
    """
    # La permission est explicitement définie sur `AllowAny`.
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Product.
    Fournit des actions CRUD complètes (list, create, retrieve, update, destroy).
    
    SECURITE: Cette vue n'a pas de `permission_classes` défini.
    Elle utilise donc la configuration par défaut de `settings.py`,
    qui est `IsAuthenticated`. Par conséquent, toutes les routes
    de ce ViewSet nécessitent un token JWT valide pour être accessibles.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]