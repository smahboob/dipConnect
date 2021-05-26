from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_token
from django.template.defaultfilters import slugify

# blank = True means that field is empty

class Profile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) #every user has only one profile
    bio = models.TextField(max_length=300, default="No bio", blank=True)
    email = models.EmailField(max_length=200)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default = "avatar.png", upload_to='avatars')
    #install pillow, create media root , inside media root put avatar png
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}-{self.created}" 

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
        super().save(*args, **kwargs)