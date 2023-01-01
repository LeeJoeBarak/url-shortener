from django.shortcuts import render
from django.shortcuts import redirect as redir
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
import random, string, json

from django.views.decorators.csrf import csrf_exempt

from .models import ShortURL


BASE_URL = "http://localhost:8000/"

# Create your views here.
def home(request):
    return render(request, 'home.html')


@csrf_exempt
def createShortURL(request):
    """
    run the following cmd to address this route:

    $ curl - X POST
    "http://localhost:8000/create"
    - H "Content-Type: application/json"
    - d "{\"url\": \"https://ravkavonline.co.il\"}"
    """

    if request.method == 'POST':
        # Parse the JSON payload and get the long URL
        data = json.loads(request.body.decode('utf-8'))
        try:
            # url = data.get('url')
            url = data['url']
        except:
            return HttpResponseBadRequest('Invalid data fields or missing data fields')
        random_chars_list = list(string.ascii_letters)
        short_url = ''
        for i in range(6):
            short_url += random.choice(random_chars_list)
        while len(ShortURL.objects.filter(short_url=short_url)) != 0:
            short_url = ''
            for i in range(6):
                short_url += random.choice(random_chars_list)
        short_url_record = ShortURL(url=url, short_url=short_url, hit_count=0)
        short_url_record.save()
        return JsonResponse({'short_url': BASE_URL+short_url})
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
