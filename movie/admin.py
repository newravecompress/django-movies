from django.contrib import admin

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Review

admin.site.register(RatingStar)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'url'
    list_display_links = 'id', 'name', 'url'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'email', 'parent', 'movie',
    readonly_fields = 'name', 'email'


class ReviewList(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = 'name', 'email',


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = 'title', 'category', 'url', 'draft'
    list_display_links = 'title', 'url'
    list_filter = 'category', 'year'
    list_editable = 'draft',
    search_fields = 'title', 'category__name',
    inlines = [ReviewList]
    save_on_top = True
    save_as = True
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': ('description', 'poster',)
        }),
        (None, {
            'fields': (('year', 'country', 'world_premiere'),)
        }),
        ('Actors and directors', {
            'classes': ('collapse',),
            'fields': (('actors', 'directors'),)
        }),
        ('Genres and category', {
            'classes': ('collapse',),
            'fields': (('genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)
        }),
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = 'name', 'url',


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = 'name', 'age'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = 'star', 'ip', 'movie'


@admin.register(MovieShots)
class RatingAdmin(admin.ModelAdmin):
    list_display = 'title', 'movie'
