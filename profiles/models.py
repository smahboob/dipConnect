from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_token
from django.template.defaultfilters import slugify

# blank = True means that field is empty

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

    def get_friends(self):
        return self.friends.all()

    def get_total_number_of_friends(self):
        return self.friends.all().count()
    
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

class Relationship(models.Model):
    #evertime a profile is deleted, remove the relationship also
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender') #who sends the invite
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver') #who receives it
    status = models.CharField(max_length=8, choices=STATUS_CHOICES) #if accepted, ignored, deleted, if accepted, we need signal to increase friends.
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"