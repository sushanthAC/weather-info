from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

def index (request):
	url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=b3e28a639c62a33ad1512266c6b5bc72'

	cities = City.objects.all()
	if request.method == 'POST':
		response = requests.get(url.format(request.POST['name'])).json()
		if (response['cod'] != '404'):
			form = CityForm(request.POST)
			form.save()

	form = CityForm()

	weather_data = []
	for city in cities:		
		response = requests.get(url.format(city)).json()
		is_error = 0
		error_message = ''
		if (response['cod'] == '401'):
			is_error = 1		
			error_message = response['message']
		elif (response['cod'] == '404'):
			error_message = response['message']
		else:
			city_weather = {
				'city' : city,
				'temperature': response['main']['temp'],
				'description' : response['weather'][0]['description'],
				'icon': response['weather'][0]['icon'],	
			}
			weather_data.append(city_weather)
		
	context = {'weather_data' : weather_data, 'status' : is_error, 'error_message' : error_message, 'form' : form}
	return render(request, 'weather/index.html', context)
