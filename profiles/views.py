from django.shortcuts import render
from .models import Profile
from .forms import ProfileModelForm

# Create your views here.
#PART4 start

def my_profile_view(request):
    #get the profile based on the logged in user. 
	profile_obj = Profile.objects.get(user=request.user)						

 	#this is for letting user update, we have defined it in forms.py in profiles project., instance tells update this profile 
	form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile_obj)						
	
	#this is a flag which changes to true, if conditions met
	confirm = False
	failed_to_update = False
 
	if(request.method == 'POST'):
		if(form.is_valid()):
			form.save()
			confirm = True
		else:
			failed_to_update = True

	context = {
		'profile_obj':profile_obj,
		'form': form,
		'confirm': confirm,
		'failed_update': failed_to_update,
	}

	return render(request, 'profiles/userProfile.html', context)