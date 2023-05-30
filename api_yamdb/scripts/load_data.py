from csv import DictReader

from reviews.models import (
    User, Title, Genre, Category, Review, Comment
)

TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Genre: 'genre.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    Title.genre.through: 'genre_title.csv',

}

FOREIGN_KEYS = {
    'author': 'author_id',
    'category': 'category_id',
}


def run():
    for model, file in TABLES.items():

        with open(
            f'static/data/{file}', encoding='utf-8'
        ) as csv_data:

            reader = DictReader(csv_data)
            for fieldname in reader.fieldnames:
                if fieldname in FOREIGN_KEYS:

                    index = reader.fieldnames.index(fieldname)
                    reader.fieldnames[index] = FOREIGN_KEYS[fieldname]

            model.objects.bulk_create(model(**data) for data in reader)
