from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    cities = City.objects.all()

    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    weather_data = []

    for city in cities:
        city_weather = requests.get(
            url.format(city)).json()

        weather = {
            'city': city,
            'temperature': int(((city_weather['main']['temp'])-32) * 5.0/9),
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }

        weather_data.append(weather)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)