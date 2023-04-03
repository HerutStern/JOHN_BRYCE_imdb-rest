import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

def validate_birth_year(val):
    if val[int('birth_year')] > datetime.datetime.today().year - 5:
        raise ValidationError('The actor is too young')

class Actor(models.Model):

    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    birth_year = models.IntegerField(db_column='birth_year', null=False, validators=[validate_birth_year])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'actors'



class Movie(models.Model):

    name = models.CharField(max_length=256, db_column='name', null=False)
    description = models.TextField(db_column='description', null=False)
    duration_in_min = models.FloatField(db_column='duration', null=False)
    release_year = models.IntegerField(db_column='year', null=False)
    pic_url = models.URLField(max_length=512, db_column='pic_url', null=True)

    actors = models.ManyToManyField(Actor, through='MovieActor')

    # def __str__(self):
    #     return self.name

    class Meta:
        db_table = 'movies'


class Rating(models.Model):

    movie = models.ForeignKey(
        'Movie',
        on_delete=models.CASCADE,
    )
    rating = models.SmallIntegerField(db_column='rating', null=False,
                validators=[MinValueValidator(1), MaxValueValidator(10)])
    rating_date = models.DateField(db_column='rating_date', null=False, auto_now_add=True)


    class Meta:
        db_table = 'ratings'


class MovieActor(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    salary = models.IntegerField()
    main_role = models.BooleanField(null=False, blank=False)

    def __str__(self):
        return f"{self.actor.name} in movie {self.movie.name}"


    class Meta:
        db_table = 'movie_actors'