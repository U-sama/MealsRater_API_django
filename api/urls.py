from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import RatingViewSet, MealViewSet

router = routers.DefaultRouter()
router.register('ratings', RatingViewSet)
router.register('meals', MealViewSet)


urlpatterns = [
    path('', include(router.urls)),

]
