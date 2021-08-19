from __future__ import annotations
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.http import HttpRequest

from .models import Movie


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(DetailView):
    """Детальная фильма"""
    model = Movie
    slug_field = 'url'
