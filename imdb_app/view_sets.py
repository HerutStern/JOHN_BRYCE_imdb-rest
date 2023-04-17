from rest_framework.viewsets import ModelViewSet

from imdb_app.models import Movie, Actor
from imdb_app.serializers import MovieSerializer, ActorSerializer


class MovieViewSet(ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

class ActorViewSet(ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()