from __future__ import annotations
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpRequest

from .models import Movie


class MoviesView(View):
    """Список фильмов"""
    def get(self, request: HttpRequest):
        movies = Movie.objects.all()
        return render(request, 'movie/movie_list.html', {'movie_list': movies})
