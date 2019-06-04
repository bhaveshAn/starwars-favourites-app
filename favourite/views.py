from django.http import JsonResponse
from django.shortcuts import render
from django.urls import resolve
from django.core import serializers
import json
import requests
import uuid

from favourite.models import FavouriteMovies, FavouritePlanets, SavedPlanets


def index(request):
    """
    This is a view concerning movies. It supports 2 methods:

    GET : Getting the list of all the movies
    POST : POST used to set any movie as favourite.
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            user = body["guest"]
            movie = body["movie"]
            release = body["release"]
            if FavouriteMovies.objects.filter(user=user, movie=movie, release=release):
                response_data = {}
                response_data["result"] = "Already exist"
                return JsonResponse(response_data, status=403)
            else:
                favourite = FavouriteMovies.objects.create(
                    user=user, movie=movie, release=release
                )
                if favourite.pk is not None:
                    response_data = {}
                    response_data["result"] = "success"
                else:
                    response_data = {}
                    response_data["result"] = "error"
                return JsonResponse(response_data, status=200)
        except Exception:
            return JsonResponse({}, status=500)
    elif request.method == "GET":
        try:
            r = requests.get("https://swapi.co/api/films/")
            if r.json():
                if request.COOKIES.get("guest_id"):
                    guest_id = request.COOKIES.get("guest_id")
                    favourited = serializers.serialize(
                        "json", FavouriteMovies.objects.filter(user=guest_id)
                    )
                    context = {
                        "allmovies": r.json(),
                        "guest_id": guest_id,
                        "favourited": favourited,
                    }
                    response = render(request, "favourite/movies.html", context)
                else:
                    guest_id = uuid.uuid1().hex
                    favourited = ""
                    context = {
                        "allmovies": r.json(),
                        "guest_id": guest_id,
                        "favourited": favourited,
                    }
                    response = render(request, "favourite/movies.html", context)
                    response.set_cookie(
                        "guest_id", guest_id, max_age=730 * 24 * 60 * 60
                    )

            else:
                response = render(request, "favourite/movies.html", {})
            return response
        except Exception:
            response = render(request, "favourite/movies.html", {})
            return response


def planets(request):
    """
    This is a view concerning planets. It supports 2 methods:

    GET : Getting the list of all the planets
    POST : POST used to set any planet as favourite.
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            user = body["guest"]
            planet = body["planet"]
            population = body["population"]
            if (
                FavouritePlanets.objects.filter(
                    user=user, planet=planet, population=population
                )
            ) and "is_favourite" in body:
                response_data = {}
                response_data["result"] = "Already exist"
                return JsonResponse(response_data, status=403)
            elif (
                SavedPlanets.objects.filter(
                    user=user, planet=planet, population=population
                )
            ) and "is_save" in body:
                response_data = {}
                response_data["result"] = "Already exist"
                return JsonResponse(response_data, status=403)
            else:
                if "is_favourite" in body:
                    favourite = FavouritePlanets.objects.create(
                        user=user, planet=planet, population=population
                    )
                    if favourite.pk:
                        response_data = {}
                        response_data["result"] = "success"
                    else:
                        response_data = {}
                        response_data["result"] = "error"
                    return JsonResponse({"result": response_data}, status=200)
                elif "is_save" in body:
                    save = SavedPlanets.objects.create(
                        user=user, planet=planet, population=population
                    )
                    if save.pk:
                        response_data = {}
                        response_data["result"] = "success"
                    else:
                        response_data = {}
                        response_data["result"] = "error"
                    return JsonResponse({"result": response_data}, status=200)
        except Exception:
            return JsonResponse({}, status=500)
    elif request.method == "GET":
        try:
            r = requests.get("https://swapi.co/api/planets/")
            if r.json():
                if request.COOKIES.get("guest_id"):
                    guest_id = request.COOKIES.get("guest_id")
                    favourited = serializers.serialize(
                        "json", FavouritePlanets.objects.filter(user=guest_id)
                    )
                    saved = serializers.serialize(
                        "json", SavedPlanets.objects.filter(user=guest_id)
                    )
                    context = {
                        "allPlanets": r.json(),
                        "guest_id": guest_id,
                        "favourited": favourited,
                        "saved": saved,
                    }
                    response = render(request, "favourite/planets.html", context)
                else:
                    guest_id = uuid.uuid1().hex
                    favourited = ""
                    saved = ""
                    context = {
                        "allPlanets": r.json(),
                        "guest_id": guest_id,
                        "favourited": favourited,
                        "saved": saved,
                    }
                    response = render(request, "favourite/planets.html", context)
                    response.set_cookie(
                        "guest_id", guest_id, max_age=730 * 24 * 60 * 60
                    )
            else:
                response = render(request, "favourite/planets.html", {})
            return response
        except Exception:
            response = render(request, "favourite/planets.html", {})
            return response


def favourited(request):
    """
    This is a view concerning favourited movies & planets.
    It supports 2 methods:

    GET : Getting the list of all the favourite movies & planets
    POST : POST used to unset any movie or planet from favourite.
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            user = body["guest"]
            element = body["element"]
            planet = body["planet"]
            movie = body["movie"]
            if element:
                favourite = FavouritePlanets.objects.get(
                    user=user, planet=planet
                ).delete()
            else:
                favourite = FavouriteMovies.objects.get(user=user, movie=movie).delete()
            if favourite:
                response_data = {}
                response_data["result"] = "success"
            else:
                response_data = {}
                response_data["result"] = "error"
            return JsonResponse(response_data, status=200)
        except Exception:
            return JsonResponse({}, status=500)
    if request.method == "GET":
        try:
            if request.COOKIES.get("guest_id"):
                guest_id = request.COOKIES.get("guest_id")
                if resolve(request.path_info).url_name == "favouritedplanets":
                    favourited = serializers.serialize(
                        "json", FavouritePlanets.objects.filter(user=guest_id)
                    )
                    context = {
                        "favourited": json.loads(favourited),
                        "guest_id": guest_id,
                    }
                else:
                    favourited = serializers.serialize(
                        "json", FavouriteMovies.objects.filter(user=guest_id)
                    )
                    context = {
                        "favourited": json.loads(favourited),
                        "guest_id": guest_id,
                    }
            else:
                context = {}
            response = render(request, "favourite/favourited.html", context)
            return response
        except Exception:
            response = render(request, "favourite/favourited.html", {})
            return response


def saved(request):
    """
    This is a view concerning saved planets.
    It supports 2 methods:

    GET : Getting the list of all the saved planets
    POST : POST used to unset any planet from saved.
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            user = body["guest"]
            element = body["element"]
            planet = body["planet"]
            if element:
                saved = SavedPlanets.objects.get(user=user, planet=planet).delete()
            if saved:
                response_data = {}
                response_data["result"] = "success"
            else:
                response_data = {}
                response_data["result"] = "error"
            return JsonResponse(response_data, status=200)
        except Exception:
            return JsonResponse({}, status=500)
    if request.method == "GET":
        try:
            if request.COOKIES.get("guest_id"):
                guest_id = request.COOKIES.get("guest_id")
                if resolve(request.path_info).url_name == "savedplanets":
                    saved = serializers.serialize(
                        "json", SavedPlanets.objects.filter(user=guest_id)
                    )
                    context = {"saved": json.loads(saved), "guest_id": guest_id}
            else:
                context = {}
            response = render(request, "favourite/saved.html", context)
            return response
        except Exception:
            response = render(request, "favourite/saved.html", {})
            return response


def search(request):
    """
    This is a view concerning search. It supports 2 methods:

    GET : Getting the list of all the planets with a queried title.
    POST : POST used to search for a planet using its title.
    """

    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            user = body["guest"]
            planet = body["planet"]
            population = body["population"]
            if FavouritePlanets.objects.filter(
                user=user, planet=planet, population=population
            ):
                response_data = {}
                response_data["result"] = "Already exist"
                return JsonResponse(response_data, status=403)
            else:
                favourite = FavouritePlanets.objects.create(
                    user=user, planet=planet, population=population
                )
                if favourite.pk is not None:
                    response_data = {}
                    response_data["result"] = "success"
                else:
                    response_data = {}
                    response_data["result"] = "error"
                return JsonResponse(response_data, status=200)
        except Exception:
            return JsonResponse({}, status=500)
    elif request.method == "GET":
        try:
            payload = {"search": request.GET.get("query")}
            r = requests.get("https://swapi.co/api/planets/", params=payload)
            if r.json():
                if request.COOKIES.get("guest_id"):
                    guest_id = request.COOKIES.get("guest_id")
                    favourited = serializers.serialize(
                        "json", FavouritePlanets.objects.filter(user=guest_id)
                    )
                    context = {
                        "allPlanets": r.json(),
                        "guest_id": guest_id,
                        "favourited": favourited,
                    }
                    response = render(request, "favourite/planets.html", context)
                else:
                    guest_id = uuid.uuid1().hex
                    favourited = ""
                    context = {
                        "allPlanets": r.json(),
                        "guest_id": guest_id,
                        "favourited": favourited,
                    }
                    response = render(request, "favourite/planets.html", context)
                    response.set_cookie(
                        "guest_id", guest_id, max_age=730 * 24 * 60 * 60
                    )
            else:
                context = {}
                response = render(request, "favourite/planets.html", context)
            return response
        except Exception:
            context = {}
            response = render(request, "favourite/planets.html", context)
            return response
