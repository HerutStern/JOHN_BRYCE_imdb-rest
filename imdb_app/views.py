from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request


from imdb_app.models import *
from imdb_app.serializers import *

from django.db.models import Avg


# Create your views here.

# @api_view(['GET'])
# def get_movies(request):
#     all_movies = Movie.objects.all()
#     data = []
#     for movie in all_movies:
#         data.append({
#             'id': movie.pk,
#             'name': movie.name,
#             'release_year': movie.release_year,
#             'description': movie.description,
#             'duration_in_min': movie.duration_in_min,
#             'actors': []
#         })
#     return Response(data=data)


@api_view(['GET', 'POST'])
def get_movies(request: Request):

    if request.method == 'GET':
        all_movies = Movie.objects.all()
        print("initial query:", all_movies.query)

        if 'name' in request.query_params:
            all_movies = all_movies.filter(name__iexact=request.query_params['name'])
            print("after adding name filter", all_movies.query)
        if 'duration_from' in request.query_params:
            all_movies = all_movies.filter(duration_in_min__gte=request.query_params['duration_from'])
            print("after adding duration_from filter", all_movies.query)
        if 'duration_to' in request.query_params:
            all_movies = all_movies.filter(duration_in_min__lte=request.query_params['duration_to'])
            print("after adding duration_to filter", all_movies.query)
        if 'description' in request.query_params:
            all_movies = all_movies.filter(description__icontains=request.query_params['description'])
            print("after adding description filter", all_movies.query)

        serializer = MovieSerializer(instance=all_movies, many=True)
        return Response(data=serializer.data)
    else:
        serializer = CreateMovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def get_movie(request, movie_id):
    # try:
    #     movie = Movie.objects.get(id=movie_id) #object Movie
    # except Movie.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    movie = get_object_or_404(Movie, id=movie_id)
    serializer = DetailedMovieSerializer(instance=movie)
    return Response(data=serializer.data)

@api_view(['GET'])
def get_movie_actors(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)
    all_casts = movie.movieactor_set.all()
    serializer = CastSerializer(instance=all_casts, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def get_actors(request):
    all_actors = Actor.objects.all()
    serializer = ActorSerializer(instance=all_actors, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def get_ratings(request):
    all_ratings = Rating.objects.all()
    serializer = RatingSerializer(instance=all_ratings, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def get_movie_ratings(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    serializer = RatingSerializer(
        instance=movie.rating_set.all(), many=True)
    return Response(data=serializer.data)

@api_view(['GET'])
def get_avg_movie_rating(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    avg_rating = movie.rating_set.aggregate(Avg('rating'))
    print(avg_rating)
    return Response(avg_rating)