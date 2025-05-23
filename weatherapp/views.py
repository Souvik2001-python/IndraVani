from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

# Create your views here.
def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Kolkata'
    
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=56bd174007a40af97526edb028b2ddbe'
    PARAMS = {'units': 'metric'}

    # API set for background images
    API_KEY = 'AIzaSyAqGbj19Qv-4nsGB7-LvAj7LPtTssXpdWg'
    SEARCH_ENGINE_ID = '21acc89b522264ccf'
    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    data = requests.get(city_url).json()
    search_items = data.get("items")

    # ✅ Safely get image_url or set a fallback
    if search_items and len(search_items) > 1:
        image_url = search_items[1]['link']
    else:
        image_url = 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600'

    # storing the data from the api
    try:
        data = requests.get(url, PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except KeyError:
        exception_occurred = True
        messages.error(request, 'The data for the entered city is not available at this time !!')
        day = datetime.date.today()
        return render(request, 'weatherapp/index.html', {
            'description': 'Clear Sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'Kolkata',
            'exception_occurred': exception_occurred,
            'image_url': image_url
        })
