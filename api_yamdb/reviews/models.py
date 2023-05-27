from django.db import models

from users.models import User


class Genre(models.Model):
    """
    Информация о жанре произведения
    """
    slug = models.CharField(
        max_length=50
    )
    name = models.CharField(
        max_length=256
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Category(models.Model):
    """
    Категория произведения (литературное, музыкальное и т.д.)
    """
    slug = models.CharField(
        max_length=50
    )
    name = models.CharField(
        max_length=256
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Общая информация о произведении
    """
    name = models.CharField(max_length=256)
    year = models.IntegerField()  # Год выпуска
    genre = models.ManyToManyField(
        Genre, related_name='titles', verbose_name='Жанр')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles',
        verbose_name='Категория', null=True)
    description = models.TextField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Review model."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение')
    text = models.TextField()
    score = models.IntegerField(
        'Оценка',
        default=0
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_pair_author_title'
            )
        ]

    def __str__(self):
        return (
            f'Отзыв {self.text[:20]} от {self.author} на {self.title} '
            f'{self.pub_date}'
        )


class Comment(models.Model):
    """Comment model."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['id']
