from django.shortcuts import render,redirect
from .models import Post, Profile, Like, Comment

# Create your views here.

def post_comment_create_and_list(request):
    query_set = Post.objects.all()      #store all the post objects in query set
    profile = Profile.objects.get(user=request.user)
    context  = {
        'query_set': query_set,
        'profile':profile,
    }
    
    return render(request, 'posts/main.html', context)

def like_unlike_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_object = Post.objects.get(id = post_id)
        profile = Profile.objects.get(user=user)
        
        #if profile has already like the post, unlike it
        if profile in post_object.liked.all():
            post_object.liked.remove(profile)
        else:
            post_object.liked.add(profile)
            
        like, created = Like.objects.get_or_create(user=profile, post_id = post_id)
        
        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
        
        else:
            like.value == "Like"
        
            post_object.save()
            like.save()
        
            
    return redirect('posts:main-post-view')