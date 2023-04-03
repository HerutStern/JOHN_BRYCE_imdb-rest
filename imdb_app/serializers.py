from django.core.validators import MinValueValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from imdb_app.models import Movie, Actor, MovieActor, Rating


# class MovieSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     release_year = serializers.IntegerField()
#     description = serializers.CharField()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # fields = '__all__'
        fields = ['id', 'name', 'release_year', 'duration_in_min', 'pic_url']
        # exclude = ['pic_url']
        # depth = 1


class DetailedMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ['actors']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieActor
        # fields = '__all__'
        exclude = ['id', 'movie']
        depth = 1


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ['id', 'movie']


class CreateMovieSerializer(serializers.ModelSerializer):
    # name = models.CharField(max_length=256, db_column='name', null=False)
    # description = models.TextField(db_column='description', null=False)
    # duration_in_min = models.FloatField(db_column='duration', null=False)
    # release_year = models.IntegerField(db_column='year', null=False)
    # id = serializers.IntegerField(read_only=True)
    # release_year = serializers.IntegerField(
    #     validators=[MinValueValidator(1800)]
    # )
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'duration_in_min', 'release_year']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def validate(self, attrs):
        if attrs['release_year'] <= 1920 and attrs['duration_in_min'] >= 60:
            raise ValidationError('Old movies supposed to me short')
        return attrs

# actor
class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'birth_year']
        # exclude = ['pic_url']
        # depth = 1