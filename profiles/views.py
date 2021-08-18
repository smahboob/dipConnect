from django.shortcuts import render
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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


#profile list view inherits from the list view
class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'query_set'
    
    def get_queryset(self):
        query_set = Profile.objects.get_all_profiles(self.request.user)
        return query_set
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)	#this is the current users profile
        
        #if u are a receiver of a request
        rel_r = Relationship.objects.filter(sender=profile)
        rel_receiver = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        context["rel_receiver"] = rel_receiver

        #if u are a sender of a request
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_sender = []
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_sender"] = rel_sender
        
        #check if the context is empty
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context
    

#PART11-12    
@login_required
def send_invatation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')
    
@login_required
def remove_from_friends(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')