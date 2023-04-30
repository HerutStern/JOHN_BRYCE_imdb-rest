import django_filters
from django.db.models import Count, OuterRef, Subquery
from django.http import JsonResponse
from django_filters import FilterSet
from rest_framework import mixins, status
from rest_framework.authtoken.admin import User
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.core.exceptions import ValidationError


from imdb_app.models import Movie, Actor, Directors, Oscars
from imdb_app.serializers import MovieSerializer, DetailedMovieSerializer, CreateMovieSerializer, CastSerializer, \
    ActorSerializer, DirectorsSerializer, OscarsSerializer, SignupSerializer


# users:

class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return view.action == 'create' and request.data['is_staff'] and request.user.is_staff

class UsersViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = SignupSerializer
    queryset = User.objects.all()
    permission_classes = [UserPermission]

# movie:

class MovieFilterSet(FilterSet):

    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    duration_from = django_filters.NumberFilter('duration_in_min', lookup_expr='gte')
    duration_to = django_filters.NumberFilter('duration_in_min', lookup_expr='lte')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ['release_year']

class MoviePermission(BasePermission):

    def has_permission(self, request, view):
        print("inside has_permission")
        return request.user.is_staff or view.action \
            in ('list', 'retrieve')

    def has_object_permission(self, request, view, obj):
        print("inside has_object_permission", obj)
        return view.action == 'retrieve' or \
            obj.created_by == request.user
        # obj.created_by_id == request.user.id

class MovieViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    filterset_class = MovieFilterSet
    permission_classes = [MoviePermission]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedMovieSerializer
        elif self.action == 'create':
            return CreateMovieSerializer
        else:
            return super().get_serializer_class()

        # def get_permissions(self):
        #     if self.action in ('create', 'update', 'destroy'):
        #         return [IsAdminUser()]
        #     else:
        #         return []

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
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(methods=['GET'], detail=True, url_path='years/<oscar_year>')
    def get_year(self, request, *args, **kwargs):
        oscar_year = kwargs['oscar_year']
        queryset = self.get_queryset().filter(ceremony_year=oscar_year)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, url_path='movie_with_most_oscars ')
    def get_movie_with_most_oscars(self):
        qs = Oscars.objects.all().annotate().order_by('movie_id')
        data = {}
        if qs.exists():
            most_common_movie_id = qs.first().movie_id
            movie = Movie.objects.get(id= most_common_movie_id)
            data['movie_id'] = most_common_movie_id
            movie_serializer = MovieSerializer(movie)
            data['movie_name'] = movie_serializer.data['name']
        else:
            data = None
        return JsonResponse(data)
    @action(methods=['GET'], detail=True, url_path='actor_with_most_oscars ')
    def get_actor_with_most_oscars (self, request, *args, **kwargs):
        pass

    @action(methods=['GET'], detail=True, url_path='total_oscars ')
    def get_total_oscars (self, request, *args, **kwargs):
        pass

