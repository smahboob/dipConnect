github repo: https://github.com/hellopyplane/Social-Network/tree/master/profiles

1. Profiles
	-profile
	-relationship between profile, how to make friends, how to remove friends. 

2. Posts
	-post
	-comment
	-like

3. Allauth (authnetication system)
	-using django signals, we can send information to an app when events are created 


superuser details. other user details for testing
	smahboob1
	saadmahboob3@gmail.com
	okay4092

	testUser1
	okay4092

u can create a test user, 
	and then generate a profile for them


run the server on python3 manage.py runserver and take a look the urls
		http://127.0.0.1:8000/profiles/myprofile/
		http://127.0.0.1:8000/
		http://127.0.0.1:8000/admin/

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Implemented uptil now,
	profiles, relationships, send and accept request udpates, signal receivers to create user profiles and update relationships
	created html files for base, nav, and extended to home and profile
	last left on editing profile.html where all info and image should show. 


Started on Part-5 on Sat, July 3rd. (From the profiles page and form)

#go to settings and clear the cookies or history if static files such as style.css or main_javascript.js are not working. 
ended part 5
finished implemneting the profile url,used semantic ui
semantic ui = https://semantic-ui.com/elements/
overriding the semantic ui: https://stackoverflow.com/questions/55005996/overriding-styles-in-semantic-ui-react

created a POST form, to show an update popup and update the profile information. 
created Post model, like model and comment models, and displayed also

finished implementing new comment, new post and show comment
fix the ui later, basic form functionality is working for now. 

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Start working on
	Part 9
	https://www.youtube.com/watch?v=UAwxz0LogqE&list=PLgjw1dR712joFJvX_WKIuglbR1SNCeno1&index=9

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Notes

	tagging system
	https://dev.to/coderasha/how-to-add-tags-to-your-models-in-django-django-packages-series-1-3704

	if u change anything in models, call 
										python3 manage.py makemigrations
										python3 manage.py migrate
										run server again