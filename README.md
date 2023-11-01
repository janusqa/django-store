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
$ python manage.py makemigrations # generates a new migration, can be ran multiple times as you change your models.  Then use below command to generate the schema
$ python manage.py migrate # generate schema from migrations above.

Revert a migration
---
$ python manage.py migrate <app-folder-name> <migration-number> # where xxxx is the migration number for that specific app in the migrations folder
eg $ python manage.py migrate store 0003

Now delete the migration file and roll back via git or manually to remove
code you are reverting in the models
$ git reset --hard HEAD~1
or find the hash of commit to be rolled back to  and ...
$ git reset --hard <hash>

ADD CUSTOM MIGRATION
---
1) create empty migration
   $ python manage.py makemigrations store --empty
2) in the newly created migrations file in the operations array
   eg. 
       operations = [
        migrations.RunSQL(
            """
            INSERT INTO store_collection (title)
            VALUES ("collection1")
            """,
            """
            DELETE FROM store_collection WHERE title="collection1"
            """
        )
       ]
    NOTE: the second arg to RunSQL is a sql statment that reverts the first statement.  We need it so we can use migrations to revert. 
    The first arg migrates forwards to the new state of the db, the second 
    arg migrates backward to the past state of the db
    