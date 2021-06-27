#Started in Part4
from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
	#return HttpResponse("Hello World")
	user = request.user
	hello = 'Hello World'
	context = {'user': user, 'hello':hello} #dict of key value pairs

	return render(request, 'main/home.html', context) #this would render the home page html file