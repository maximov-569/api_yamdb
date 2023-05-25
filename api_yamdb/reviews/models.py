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
    name = models.CharField(max_length=200)
    author = models.TextField(max_length=200)
    year = models.IntegerField()  # Год выпуска
    genre = models.ManyToManyField(Genre, related_name='titles', verbose_name='Жанр')
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, related_name='titles',
                                 verbose_name='Категория')

    def __str__(self):
        return self.name
