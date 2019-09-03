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
    path('books/modify/', views.ModifyBook.as_view(), name='modify_book'),
    path("books/modify/<path:book_id>/", views.book_modifier, name='book_modifier'),
    path('books/delete/', views.DeleteBook.as_view(), name='delete_book'),
    path("books/<path:book_id>/", views.BookInfo.as_view(), name='book_info'),
    path('locations/', views.LocationsView.as_view(), name='locations'),
    path('locations/new/', views.NewLocation.as_view(), name='new_location'),
    path('locations/delete/', views.DeleteLocation.as_view(), name='delete_location'),
    path('loans/', views.LoansView.as_view(), name='loans'),
    path('loans/loan/', views.LoanBook.as_view(), name='loan_book'),
    path('loans/return/', views.ReturnBook.as_view(), name='return_book'),
]
