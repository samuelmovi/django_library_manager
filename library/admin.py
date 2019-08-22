from django.contrib import admin
from .models import Book, Location, Loan

# Register your models here.
admin.site.register(Book)
admin.site.register(Location)
admin.site.register(Loan)
