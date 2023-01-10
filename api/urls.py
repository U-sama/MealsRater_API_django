from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import RatingViewSet, MealViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('ratings', RatingViewSet)
router.register('meals', MealViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),

]
