from django.shortcuts import render
from .models import Profile, Relationship
from .forms import ProfileModelForm

# Create your views here.
#PART4 start

#users own profile view
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


#view all invites received 
def invite_received_view(request):
    profile_obj = Profile.objects.get(user=request.user)				#convert the request user into the profile object and pass into the qs as a receiver		
    query_set = Relationship.objects.invitations_received(profile_obj)
    
    context = {
		'query_set':query_set
	}
    
    return render(request, 'profiles/friendship_invites.html', context)


#this is all the profiles
def profiles_list_view(request):
    user = request.user 								#convert the request user into the user and pass into the qs as a us		
    query_set = Profile.objects.get_all_profiles(user)
    
    context = {
		'query_set':query_set
	}
    
    return render(request, 'profiles/profile_list.html', context)


#this is all the profiles available to invite, not yet in relationship
def invite_profiles_list_view(request):
    user = request.user 								#convert the request user into the user and pass into the qs as a us		
    query_set = Profile.objects.get_all_profiles_available_to_invite(user)
    
    context = {
		'query_set':query_set
	}
    
    return render(request, 'profiles/to_invite_profile_list.html', context)