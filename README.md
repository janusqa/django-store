$ python3 -m venv venv
$ source venv/bin/activate
$ pip install django black
$ django-admin startproject storefront .
$ python manage.py runserver // to start local dev server

primary folder for this project is ./storefront.  This is not where our code goes
We need to create addtional folders, where each folder is a component of the django
app.

$ python manage.py startapp <foldername>
eg. $ python manage.py playground
 
Now in the primay folder "./storefront/settings.py"  register the new app folder by adding it's folder name to INSTALLED_APPS array

VIEWS
----
Views in django are like the api endpoints.  They take a request and return a response
After creating a view we should map it to a url that will be used by some client to made a request to the view
To do this add a "urls.py" to "playground" folder
We then need to include this in the "urls.py" in the primary folder

django debug toolbar
---
https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
$ pip install django-debug-toolbar
Now add it to INSTALLED_APPS in settings.py in primary folder
Now add a url pattern to urls.py in primary folder
path('__debug__/', include(debug_toolbar.urls))

CIRCULAR DEPENDANCIES IN MODELS
---
1) either instruct djano that we dont care to create the relationship in the other table by using param "related_name='+'"
2) or specify a custom name "related_name='custom_name'"


MIGRATIONS
---
$ python manage.py makemigrations # generates a new migration
