import django_filters
from django_filters import FilterSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from imdb_app.models import Movie, Actor, Directors, Oscars
from imdb_app.serializers import MovieSerializer, DetailedMovieSerializer, CreateMovieSerializer, CastSerializer, \
    ActorSerializer, DirectorsSerializer, OscarsSerializer


# movie:

class MovieFilterSet(FilterSet):

    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    duration_from = django_filters.NumberFilter('duration_in_min', lookup_expr='gte')
    duration_to = django_filters.NumberFilter('duration_in_min', lookup_expr='lte')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ['release_year']

class MovieViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    filterset_class = MovieFilterSet

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedMovieSerializer
        elif self.action == 'create':
            return CreateMovieSerializer
        else:
            return super().get_serializer_class()

# actor:

class ActorViewSet(ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()


# directors:

class DirectorsViewSet(ModelViewSet):
    serializer_class = DirectorsSerializer
    queryset = Directors.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return DirectorsSerializer
        else:
            return super().get_serializer_class()

# oscar:
class OscarsFilterSet(FilterSet):

    ceremony_year = django_filters.CharFilter(field_name='ceremony_year', lookup_expr='exact')
    from_year = django_filters.NumberFilter('duration_in_min', lookup_expr='gte')
    to_year = django_filters.NumberFilter('duration_in_min', lookup_expr='lte')
    nomination = django_filters.CharFilter(field_name='nomination', lookup_expr='exact')
    actor_nominations = django_filters.BooleanFilter(field_name='actor',lookup_expr='isnull', exclude=True)

    class Meta:
        model = Oscars
        fields = ['ceremony_year', 'nomination', 'actor']


class OscarsViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = OscarsSerializer
    queryset = Oscars.objects.all()
    filterset_class = OscarsFilterSet

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data.copy()
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

        for oscar in data:
            movie = Movie.objects.get(id=oscar['movie'])
            movie_serializer = MovieSerializer(movie)
            oscar['movie_name'] = movie_serializer.data['name']

            actor_id = oscar['actor']
            if actor_id:
                actor = Actor.objects.get(id=actor_id)
                actor_serializer = ActorSerializer(actor)
                oscar['actor_name'] = actor_serializer.data['name']

            director_id = oscar['director']
            if director_id:
                director = Directors.objects.get(id=director_id)
                director_serializer = DirectorsSerializer(director)
                oscar['director_name'] = director_serializer.data['name']

        if page is not None:
            return self.get_paginated_response(data)
        else:
            return Response(data)

