from django.db import models


class FavouriteMovies(models.Model):
    user = models.CharField(max_length=100)
    movie = models.CharField(max_length=100)
    release = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.movie, self.release)


class FavouritePlanets(models.Model):
    user = models.CharField(max_length=100)
    planet = models.CharField(max_length=100)
    population = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.planet, self.population)


class SavedPlanets(models.Model):
    user = models.CharField(max_length=100)
    planet = models.CharField(max_length=100)
    population = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.planet, self.population)
