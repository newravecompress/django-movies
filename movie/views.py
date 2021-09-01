from __future__ import annotations

from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.http import HttpRequest, JsonResponse

from .models import Movie, Category, Actor, Genre
from .forms import ReviewForm


class GenreYear:
    """Жанры и годы выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MoviesView(ListView, GenreYear):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(DetailView, GenreYear):
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


class ActorView(DetailView, GenreYear):
    """Информация об актере"""
    model = Actor
    template_name = 'movie/actor.html'
    slug_field = 'name'


class FilterMovieView(ListView, GenreYear):
    """Фильтр фильмов"""

    def get_queryset(self):
        years = self.request.GET.getlist('year')
        genres = self.request.GET.getlist('genre')
        queryset = Movie.objects.filter(Q(year__in=years) | Q(genres__in=genres))

        return queryset


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""

    def get_queryset(self):
        years = self.request.GET.getlist('year')
        genres = self.request.GET.getlist('genre')
        queryset = Movie.objects.filter(
            Q(year__in=years) | Q(genres__in=genres)
        ).distinct().values('title', 'tagline', 'url', 'poster')
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({'movies': queryset}, safe=False)
