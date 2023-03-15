from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title

admin.site.register([Category, Comment, Review, Title, Genre])
