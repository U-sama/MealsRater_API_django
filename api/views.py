from django.shortcuts import render
from rest_framework import viewsets , status
from .models import Rating, Meal
from .serializers import RatingSerializer, MealSerializer, UserSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import request
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

from rest_framework.authtoken.models import Token


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
            'token': token.key,
        }, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        response = {
            'message': 'This is not how you should update\create rating'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # to prevent users from rating using rating view
    def update(self, request, *args, **kwargs):
        response = {
            'message': 'This is not how you should update\create rating'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # to prevent users from rating using rating view
    def create (self, request, *args, **kwargs):
        response = {
            'message': 'This is not how you should update\create rating'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(methods=['POST'], detail=True)
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']

            user = request.user # As user is identified from the token he sends
            print(user)
            # user_name = request.data['username']
            # user = User.objects.get(username=user_name)

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
