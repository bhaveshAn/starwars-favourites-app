from django.test.utils import setup_test_environment
from django.test import TestCase, Client
from django.urls import reverse

from .views import index, planets, favourited, saved, search


class StarWarTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse("home")
        self.planets_url = reverse("planets")
        self.favourited_planets_url = reverse("favouritedplanets")
        self.favourited_movies_url = reverse("favouritedmovies")
        self.saved_planets_url = reverse("savedplanets")
        self.search_url = reverse("search")

    def test_index(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favourite/movies.html")

    def test_movies(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favourite/movies.html")

    def test_planets(self):
        response = self.client.get(self.planets_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favourite/planets.html")

    def test_favourite_planets(self):
        response = self.client.get(self.favourited_planets_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favourite/favourited.html")

    def test_favourite_movies(self):
        response = self.client.get(self.favourited_movies_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favourite/favourited.html")

    def test_saved_planets(self):
        response = self.client.get(self.saved_planets_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favourite/saved.html")

    def test_search(self):
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favourite/planets.html")
