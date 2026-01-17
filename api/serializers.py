from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Product. Expose tous les champs.
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création d'utilisateurs (Signup).
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur en s'assurant que le mot de passe est
        correctement hashé.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
