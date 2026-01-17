from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import SignupView, HealthCheckView, ProductViewSet

# Le routeur DRF gère automatiquement les URLs pour le ViewSet Product
# (ex: /api/products/ et /api/products/<pk>/)
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Route pour le Health Check
    path('health/', HealthCheckView.as_view(), name='health-check'),
    
    # Routes pour l'authentification
    path('auth/signup/', SignupView.as_view(), name='signup'),
    # La vue de login est fournie par simple-jwt
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Inclusion des URLs générées par le routeur pour les produits
    path('', include(router.urls)),
]
