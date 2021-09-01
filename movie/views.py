from __future__ import annotations

from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.http import HttpRequest, JsonResponse, HttpResponse

from .models import Movie, Category, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_form'] = RatingForm()
        return context


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


class AddStarRating(View):
    """Добавление рейтинга к фильму"""

    def get_client_ip(self, request: HttpRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request: HttpRequest):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        return HttpResponse(status=400)
