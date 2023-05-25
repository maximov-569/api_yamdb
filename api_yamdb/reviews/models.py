from django.db import models


class Genre(models.Model):
    """
    Информация о жанре произведения
    """
    genre_name = models.CharField(max_lenth=200)

    def __str__(self):
        return self.genre_name


class Categories(models.Model):
    """
    Категория произведения (литературное, музыкальное и т.д.)
    """
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name


class Title(models.Model):
    """
    Общая информация о произведении
    """
    name = models.CharField(max_length=256, required=True)
    year = models.IntegerField(required=True)  # Год выпуска
    genre = models.ManyToManyField(Genre, related_name='titles', verbose_name='Жанр', required=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, related_name='titles',
                                 verbose_name='Категория', required=True)
    description = models.TextField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
