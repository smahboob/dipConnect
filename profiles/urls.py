from django.urls import path
from .views import my_profile_view, invite_received_view, profiles_list_view, invite_profiles_list_view, ProfileListView, send_invatation,remove_from_friends

app_name = 'profiles'

#these are all the urls coming profile/xyz
urlpatterns = [
	path('myprofile/', my_profile_view, name="my-profile-view"),	#this is to view your own profile
	path('my-invites/', invite_received_view, name="my-invites-view"),	#this is the view for the friend ship invites through the relationship manager
 	path('all-profiles/', ProfileListView.as_view(), name="all-profile-view"),	#this is the view for all the profiles 
 	path('invite-profiles/', invite_profiles_list_view, name="invite-profile-view"),	#this is the view for all the profiles that are not in relationship with ur profile yet and available to invite
    path('send-invite/', send_invatation, name='send-invite'),
    path('remove-friend/', remove_from_friends, name='remove-friend'),
]

#full path = profiles/myprofile