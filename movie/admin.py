from django.http import HttpRequest
from django.utils.safestring import mark_safe
from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Review


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


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


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = 'get_image',

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100">')

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = 'title', 'category', 'url', 'draft'
    list_display_links = 'title', 'url'
    list_filter = 'category', 'year'
    list_editable = 'draft',
    search_fields = 'title', 'category__name',
    readonly_fields = 'get_image',
    inlines = MovieShotsInline, ReviewList,
    save_on_top = True
    save_as = True
    form = MovieAdminForm
    actions = 'publish', 'unpublish'
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': ('description', ('get_image', 'poster', 'youtube'))
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

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="200">')

    get_image.short_description = 'Постер'

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        message = f'{row_update} записей обновлено'
        self.message_user(request, message)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = 'change',

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        message = f'{row_update} записей обновлено'
        self.message_user(request, message)

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = 'change',


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = 'name', 'url',


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = 'name', 'age', 'get_image',
    readonly_fields = 'get_image',

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="50">')

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = 'star', 'ip', 'movie'


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = 'title', 'movie', 'get_image'
    readonly_fields = 'get_image',

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="50">')

    get_image.short_description = 'Изображение'


admin.site.register(RatingStar)

admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'
