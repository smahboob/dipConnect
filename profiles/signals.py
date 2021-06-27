#PART3
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile,Relationship

#user needs to send information about who is being created
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
	'''
	if a user is being created here, create new instance of the user profile also automatically (PART-3, 6:00)
	print("sender: ", sender, " instance: " , instance)
		sender:  <class 'django.contrib.auth.models.User'>  instance:  testUser1 
		the above print statement would print this, for creating a new user, with username testUser1)
	'''
	if created: 
		Profile.objects.create(user=instance)

#this is a relationship signal
@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
	sender_ = instance.sender
	receiver_ = instance.receiver

	#add to the senders friends and also receivers friends, this would happend whenever send changes to accepted
	if instance.status == 'accepted':
		sender_.friends.add(receiver_.user)
		receiver_.friends.add(sender_.user)
		sender_.save()
		receiver_.save()
