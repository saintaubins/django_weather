import requests
import os
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

# tutorial from https://www.youtube.com/watch?v=v7xjdXWZafY
# deployment from https://www.youtube.com/watch?v=ex7vAsmCk8o

def index(request):
    
    WEATHER_SECRET_KEY = os.environ.get('WEATHER_API_KEY')

    

    # WEATHER_API_KEY
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID='+ WEATHER_SECRET_KEY
    # not using this line anymore it was for building out earlier in the app city = 'London'

    # old line to debug progress building
    # .... r = requests.get(url.format(city)).json()
    # print(r.text)
    # line above is a prlimanary progress statement, it doesn't work with the following lines of code.

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        #print(request.POST) used for setup
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name'].upper()
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    print(err_msg)
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

    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class

    }
    return render(request, 'weather.html', context)

def delete_city(request, city_name):

    City.objects.get(name=city_name).delete()

    return redirect('home')
