import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

# tutorial from https://www.youtube.com/watch?v=v7xjdXWZafY

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=4d830bb039412b9de8ccda2e3b32f1ba'
    # not using this line anymore it was for building out earlier in the app city = 'London'

    # old line to debug progress building
    # .... r = requests.get(url.format(city)).json()
    # print(r.text)
    # line above is a prlimanary progress statement, it doesn't work with the following lines of code.


    if request.method == 'POST':
        #print(request.POST) used for setup
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'] ,
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    # print(city_weather)
    # line above is another progress statement, just to verify, will now pass context variable
    # to the return statement below.
    # will now update weather.html

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather.html', context)
