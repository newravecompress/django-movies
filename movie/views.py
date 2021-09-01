from __future__ import annotations
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.http import HttpRequest

from .models import Movie, Category, Actor
from .forms import ReviewForm


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(DetailView):
    """Детальная фильма"""
    model = Movie
    slug_field = 'url'


class AddReview(View):
    """Отправка отзыва"""

    def post(self, request: HttpRequest, pk: int):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(pk=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(DetailView):
    """Информация об актере"""
    model = Actor
    template_name = 'movie/actor.html'
    slug_field = 'name'
