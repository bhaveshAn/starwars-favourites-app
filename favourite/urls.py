from django.conf.urls import url
from favourite import views

urlpatterns = [
    url(r"^search", views.search, name="search"),
    url(r"^favourite/planets", views.favourited, name="favouritedplanets"),
    url(r"^favourite/movies", views.favourited, name="favouritedmovies"),
    url(r"^saved/planets", views.saved, name="savedplanets"),
    url(r"^planets/", views.planets, name="planets"),
    url(r"^$", views.index, name="home"),
]
