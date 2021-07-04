from django.shortcuts import render,redirect
from .models import Post, Profile, Like, Comment
from .forms import PostModelForm, CommentModelForm

# Create your views here.

def post_comment_create_and_list(request):
    query_set = Post.objects.all()      #store all the post objects in query set
    profile = Profile.objects.get(user=request.user)
    
    #Post Forms(new post and comment)
    post_form = PostModelForm()
    comment_form = CommentModelForm()
    post_add = False
    
    profile = Profile.objects.get(user=request.user)    #get the user so we can assign that profile to new post
    
    if "submit_post_form" in request.POST:
        post_form = PostModelForm(request.POST, request.FILES)
        #save once u have assigned the author for the post
        if post_form.is_valid():
            instance = post_form.save(commit = False)
            instance.author = profile
            instance.save()
            post_form = PostModelForm()
            post_add = True
    
    if "submit_comment_form" in request.POST:
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))    #this was passed into a hidden input in html for the each object post 
            instance.save()
            comment_form = CommentModelForm()
    
    #this context is passed to html as a dict
    context  = {
        'query_set': query_set,
        'profile':profile,
        'post_form': post_form,
        'comment_form': comment_form,
        'post_add': post_add
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