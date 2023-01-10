from rest_framework import serializers
from .models import Meal, Rating
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token



class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'title', 'description','num_of_ratings', 'avg_ratings')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'stars', 'user', 'meal',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, "required":True}}

    #to make the token when the user is created (Solution did not work)
    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     token = Token.objects.create(user=user)
    #     return token
