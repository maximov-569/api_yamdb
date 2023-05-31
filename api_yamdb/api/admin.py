from django.contrib import admin

from reviews.models import Title, Genre, Category, Review, Comment


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
