from django.contrib import admin
from django.apps import apps
from django.contrib.auth.models import Group

from .models import FavouriteMovies, FavouritePlanets, SavedPlanets

admin.site.register(FavouriteMovies)
admin.site.register(FavouritePlanets)
admin.site.register(SavedPlanets)
admin.site.unregister(Group)
