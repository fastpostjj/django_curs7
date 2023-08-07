from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.db import models
from user_auth.models import User


class UsersSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'phone',
            'is_active'
        )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Сериализатор  MyTokenObtainPairSerializer
    для обработки запросов на получение токена
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token['username'] = user.username
        token['email'] = user.email
        return token

    # def get_paying(self, obj):
    #     # paying_serializers = PayingSerializers(obj.user_set.all(), many=True)
    #     # return paying_serializers.data
    #
    #     paying = obj.paying_set.all()
    #     if paying:
    #         return paying
    #     return []

    # def get_paying(self, obj):
    #     paying_serializers = PayingSerializers(obj.paying_set.all(), many=True)
    #     return paying_serializers.data
