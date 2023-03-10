from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=100,
        db_index=True)
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True)

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=100,
        db_index=True)
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True)

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Произведение',
        max_length=200,
        db_index=True)
    year = models.PositiveSmallIntegerField(
        verbose_name='Год',)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True,
        verbose_name='Категория',)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        blank=True,
        verbose_name='Жанр',
    )

    description = models.TextField(
        verbose_name='Описание',
        null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',)
    text = models.TextField(verbose_name='Отзыв',)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор',)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True)
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Минимальный рейтинг 1'),
            MaxValueValidator(10, 'Максимальный рейтинг 10')
        ]
    )

    class Meta:
        ordering = ('score',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',)
    text = models.TextField(verbose_name='Комментарий',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',)
    pub_date = models.DateField(
        verbose_name='Дата',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
