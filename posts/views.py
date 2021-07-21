from django.shortcuts import render,redirect
from .models import Post, Profile, Like, Comment
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

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


#this class based view is to delete the posts, url in urls.py
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    
    #this is where u go once successfull in deleting
    #reverse is used for function views and reverse lazy for class based view
    #another similar way is success_url = 'posts/'
    success_url = reverse_lazy('posts:main-post-view')
    
    
    #check if the author is the logged in user, other show warning
    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post to delete it!')
        return obj


#this class based view is to update the posts, url in urls.py
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostModelForm  #this is the basic view for new post that we created
    template_name = 'posts/update.html'         #this is the html file
    success_url = reverse_lazy('posts:main-post-view')
        
    #check if the author matches
    def form_valid(self, form):
        #grab the user from the profile object
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the author of the post to update it!")
            return super().form_invalid(form)