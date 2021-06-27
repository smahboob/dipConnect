from django.shortcuts import render
from .models import Profile

# Create your views here.
#PART4 start

def my_profile_view(request):
	profile_obj = Profile.objects.get(user=request.user)	#get the profile based on the logged in user. 

	context = {
		'profile_obj':profile_obj
	}

	return render(request, 'profiles/userProfile.html', context)