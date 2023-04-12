from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from imdb_app.models import *
from imdb_app.serializers import *

from django.db.models import Avg
from datetime import datetime


# Create your views here.

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def actors(request, actor_id):
    the_actor = Actor.objects(id=actor_id)
    if request.method == 'GET':
        serializer = ActorSerializer(instance=the_actor, many=True)
        return Response(data=serializer.data)
    elif request.method in ('PUT', 'PATCH'):
        serializer = ActorSerializer(
            instance=the_actor, data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
    else:
        the_actor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['DELETE'])
# def remove_actor_from_movies(actor_id, movie_id):
#     movie_actors.remove(actor_id)
#     return Response(status=status.HTTP_204_NO_CONTENT)


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
    if request.method == 'GET':
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')
        if from_date and to_date:
            all_ratings = Rating.objects.filter(rating_date__gte= from_date, rating_date__lte= to_date)
        else:
            all_ratings = Rating.objects.all()

        serializer = RatingSerializer(instance=all_ratings, many=True)
        return Response(data=serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['DELETE'])
def delete_rating(request, rating_id):
    if request.method == 'DELETE':
        rating = get_object_or_404(Rating, id=rating_id)
        rating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


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



@api_view(['POST'])
def add_actor_to_movie(request, movie_id):
    if request.method == 'POST':
        #getting the movie id
        movie = get_object_or_404(Movie, id=movie_id)

        # getting params from the body
        actor_name = request.data.get('actor_name')
        if Actor.objects.get(name=actor_name): # check if the actor name exist
            main_role = request.data.get('main_role')
            salary = request.data.get('salary')

            # adding to MovieActor the new movie - actor connection
            actor_id = Actor.objects.get(name=actor_name)
            movie_actor = MovieActor.objects.create(movie=movie, actor=actor_id, main_role=main_role, salary=salary)

            serializer = MovieActorSerializer(movie_actor)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def add_rating_to_movie(request, movie_id):

    rating = request.data.get('rating')

    if request.method == 'POST':
        get_object_or_404(Movie, id=movie_id)
        if 11 > int(rating) > 0:
            new_rating = Rating.objects.create(rating= rating, rating_date= datetime.today(), movie_id= movie_id)
            serializer = RatingSerializer(new_rating)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
