from django.urls import path
from .views import post_comment_create_and_list, like_unlike_post, PostDeleteView, PostUpdateView

app_name = 'posts'

urlpatterns = [
    #this path is for displaying the home all posts at 'posts/' page
	path('', post_comment_create_and_list, name="main-post-view"),
 	path('liked/', like_unlike_post, name="like-post-view"),
  
	#for class based view always use as_view(), this is for delete with primary key as pk
	path('<pk>/delete/', PostDeleteView.as_view(), name="post-delete"),

	#update the post with the primary key check for authentic user 
 	path('<pk>/update/', PostUpdateView.as_view(), name="post-update")
]

#this is the main page for posts