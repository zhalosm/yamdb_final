from django.contrib import admin

from .models import Category, Comment, Review, Title, Genre

admin.site.register([Category, Comment, Review, Title, Genre])
