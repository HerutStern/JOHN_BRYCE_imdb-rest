import datetime
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "imdb_rest.settings"

import django
django.setup()

from imdb_app.models import *

if __name__ == '__main__':
    movies = Movie.objects.filter(release_year__gte=2000)
    print(movies)