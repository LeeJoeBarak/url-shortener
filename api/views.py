from django.shortcuts import render
from django.shortcuts import redirect as redir
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
import random, string, json, hashlib

from django.views.decorators.csrf import csrf_exempt

from .models import ShortURL


BASE_URL = "http://localhost:8000/"

# Create your views here.
def home(request):
    return render(request, 'home.html')


def createShortURL(request):
    if request.method == 'POST':
        # Parse the JSON payload and get the long URL
        data = json.loads(request.body.decode('utf-8'))
        long_url = data.get('url')

        if not long_url:
            return HttpResponseBadRequest('Missing required field: url')

        # Generate a unique short URL string using a hashing function
        counter = 0
        while True:
            # Hash the long URL and the counter value
            hash_input = long_url + str(counter)
            hash_output = hashlib.sha1(hash_input.encode('utf-8')).hexdigest()[:8]
            short_url = 'http://localhost:8000/' + hash_output

            # Check if the short URL is already in use
            try:
                ShortURL.objects.get(short_url=short_url)
            except ShortURL.DoesNotExist:
                # The short URL is not in use, so we can use it
                break
            else:
                # The short URL is already in use, so we need to try a different one
                counter += 1

        # Create a new short URL object and save it to the database
        short_url_record = ShortURL(url=long_url, short_url=short_url, hit_count=0)
        short_url_record.save()

        # Return the short URL to the user
        return JsonResponse({'short_url': short_url})
    else:
        return HttpResponseBadRequest('Invalid request method')


def redirect(request, short_url):
    # gets executed when the client goes to "http://localhost:8000/<short_url>
    curr_obj = ShortURL.objects.filter(short_url=short_url)  # ret QuerySet of all ShortURL objects that satisfy the query
    if len(curr_obj) == 0:
        return HttpResponseNotFound("Opss... The Short URL you entered does not exist.", content_type="application/json")
    # update counter of curr_obj works
    curr_obj[0].hit_count += 1
    curr_obj[0].save()
    # redirect the user to the long url address
    response = redir(curr_obj[0].url)
    return response
