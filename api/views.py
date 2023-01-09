from django.shortcuts import render
from rest_framework import viewsets , status
from .models import Rating, Meal
from .serializers import RatingSerializer, MealSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import request
from django.contrib.auth.models import User

# Create your views here.

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    @action(methods=['POST'], detail=True)
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            user_name = request.data['username']
            user = User.objects.get(username=user_name)

            try:
                rating = Rating.objects.get(user=user.id, meal=meal.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                json = {
                    "message": "Meal rate updated",
                    "result":serializer.data
                }
                return Response(json, status=status.HTTP_202_ACCEPTED)

            except:
                rating = Rating.objects.create(user=user, meal=meal, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                rating.save()
                json = {
                    "message": "Meal rate created",
                    "result":serializer.data
                }
                return Response(json, status=status.HTTP_201_CREATED)
        
        else:
            json = {
                "message": "Stars not provided",
            }
            return Response(json, status=status.HTTP_400_BAD_REQUEST)
