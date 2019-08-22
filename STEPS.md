# FAMILY LIBRARY PROJECT (POSTGRESQL)

## PROJECT SETUP
The steps to reproduce this project are as follows:
- Create project: `django-admin startproject django_library_manager`
- Create database:
```bash
docker run --rm --name django-db -e POSTGRES_PASSWORD=mysecretpassword -v $PWD/db:/var/lib/postgresql/data -d postgres:alpine
sudo apt install postgresql-client
psql -h 172.17.0.2 -U postgres
create database library_manager;
exit
```
- Set up postgres database:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'library_manager',
        'HOST': '172.17.0.2',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword',
    }
}
```
- Add to `setting.py`: `LOGIN_REDIRECT_URL='/library/'`
- Update database to accommodate changes made (aka migrate): `python manage.py migrate`
- Create admin user: `python manage.py createsuperuser`

## APP SETUP
- Create app: `python manage.py startapp library`
- Add `library.apps.LibraryConfig` to `INSTALLED_APPS` in settings.py

## MODELS
- Create models (library/models.py)
	- books
	- locations
	- loans
- Update database to accommodate new models:
    - `python manage.py makemigrations library`
    - To preview sql changes: ` python manage.py sqlmigrate library 0001 `
    - `python manage.py migrate`
- Make models available to admin user, edit library/admin.py
```pythonstub
from .models import $modelName
admin.site.register($modelName)
```

## VIEWS
- Create views for:
	- login
	- home
	- books
		- show
		- add
		- modify
		- delete
	- locations
		- show
		- add
		- modify
		- delete
	- loans
		- show
		- loan
		- return
- Create file `library/urls.py` to wire the views to the URLs:
```pythonstub
from django.urls import path
from . import views
from django.contrib.auth import views as generic_views


app_name = 'library'
urlpatterns = [
	path('', views.home, name='home'),
    path('bad_data/', views.bad_data, name='bad_data'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', generic_views.LoginView.as_view(template_name='library/login.html'), name='login'),
    path('logout/', views.log_me_out, name='log_me_out'),
    path('books/', views.BooksView.as_view(), name='books'),
    path('books/new/', views.NewBook.as_view(), name='new_book'),
    path('books/modify/', views.ModifyBook, name='modify_book'),
    path("books/modify/<path:book_id>/", views.book_modifier, name='book_modifier'),
    path('books/delete/', views.DeleteBook.as_view(), name='delete_book'),
    path('locations/', views.LocationsView.as_view(), name='locations'),
    path('locations/new/', views.NewLocation.as_view(), name='new_location'),
    path('locations/delete/', views.DeleteLocation.as_view(), name='delete_location'),
    path('loans/', views.LoansView.as_view(), name='loans'),
    path('loans/loan/', views.LoanBook.as_view(), name='loan_book'),
    path('loans/return/', views.ReturnBook.as_view(), name='return_book'),
]
```

## TEMPLATES
- Create folder `library/templates/library/` and template file for each view
- In `my_library_manager/my_library_manager/urls.py` add: `path('library/', include('library.urls')),`
- Program the views to use the templates


## STATIC FILEs
- Create folder `library/static/library/`
- Create style file `style.css`
- Within the app, it can be referred to as `library/style.css`

## TRANSLATION
- Import `from django.utils.translation import gettext as _` and wrap all your translatable string in `_()`
- In templates
	- Add `{% load i18n %}` to top of each template file using translations
	- use `{% trans 'some string' %}` or `{% trans var_name %}`
- Message file:
	- plain-text file, representing a single language, that contains all available translation strings and how they should be represented in the given language
	- Message files have a .po file extension
- Create message file:
	- install gettext
	- create folder`library/locale`
	- from `/library/` execute `django-admin makemessages -l es`
- Fill in the translations
- Execute `python manage.py compilemessages`

