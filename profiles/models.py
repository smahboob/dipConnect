from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_token
from django.template.defaultfilters import slugify
from django.db.models import Q
# blank = True means that field is empty

class ProfileManager(models.Manager):
    
    #get all profile that are not already in a frienship with ur profile
    def get_all_profiles_available_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        
        #query set for all relations where we sent or received request, which are accepted add all of them to an array
        query_set = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        accepted = []
        for relation in query_set:
            if relation.status == 'accepted':
                accepted.append(relation.receiver)
                accepted.append(relation.sender)
                
        #this contains users except us and also all that are already accepted
        available = [profile for profile in profiles if profile not in accepted]
       
        print('query_set:', query_set)
        print("accepted:", accepted)
        print("available:", available)
        
        
        return available
    
    #get all profiles except me
    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) #every user has only one profile, everytime a user is deleted, delete user
    bio = models.TextField(max_length=300, default="No bio", blank=True)
    email = models.EmailField(max_length=200)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default = "avatar.png", upload_to='avatars')

    #install pillow, create media root , inside media root put avatar png
    friends = models.ManyToManyField(User, blank=True, related_name='friends') #there can be many friends to one user
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    #profile manage
    objects = ProfileManager()

    def get_friends(self):
        return self.friends.all()

    def get_total_number_of_friends(self):
        return self.friends.all().count()
    
    def get_posts_no(self):
        return self.posts.all().count()
    
    def get_all_authors_posts(self):
        return self.posts.all()
    
    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_likes = 0
        for item in likes:
            if item.value == 'Like':
                total_likes += 1
        return total_likes
    
    def get_likes_received_no(self):
        posts = self.posts.all()        #using related name, otherwise use _set.all, related name works for reverse relation only
        total_likes = 0
        for item in posts:
            total_likes += item.liked.all().count()
        return total_likes
    
    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}" 

    def save(self, *args, **kwargs):
        ex = False
        if(self.first_name and self.last_name):
            to_slug = slugify(str(self.first_name) +  " "  + str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()

            #keep repeating until u find a unique slug using the uuid we are using in utils
            while(ex):
                to_slug = slugify(to_slug + " " + str(get_random_token()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs) #keyword args = kwargs


#tuple for relationships, one is for database, other we see
STATUS_CHOICES = (
    ('send','send'),
    ('accepted','accepted')
)



#Relationship.objeects.invitations_received(myprofile)
#we want to do this in our view
class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        query_set = Relationship.objects.filter(receiver=receiver, status='send')
        return query_set

class Relationship(models.Model):
    #evertime a profile is deleted, remove the relationship also
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender') #who sends the invite
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver') #who receives it
    status = models.CharField(max_length=8, choices=STATUS_CHOICES) #if accepted, ignored, deleted, if accepted, we need signal to increase friends.
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = RelationshipManager() #this is to initialize the manager for invitations

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"