from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

# Create your models here.

class Meal(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def num_of_ratings(self):
        ratings = Rating.objects.filter(meal=self)
        return len(ratings)

    def avg_ratings(self):
        ratings = Rating.objects.filter(meal=self)
        try: 
            return ratings.aggregate(Avg('stars'))['stars__avg']
        except:
            return 0

    def __str__(self):
        return self.title

class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    # def __str__(self):
    #     return self.meal


    class Meta:
            unique_together = (('meal', 'user'),)
            index_together = (('meal', 'user'),)



