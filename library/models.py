from django.db import models

# Create your models here.


class Location(models.Model):
    address = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    furniture = models.CharField(max_length=100)
    details = models.CharField(max_length=100)
    created = models.DateTimeField('date created')
    username = models.CharField(max_length=100)
    
    def __str__(self):
        return self.address


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    publish_date = models.CharField(max_length=50)
    purchase_date = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, null=True)
    loaned = models.BooleanField(default=False)
    created = models.DateTimeField('date created')
    modified = models.DateTimeField('date modified', null=True)
    username = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    lender = models.CharField(max_length=100)
    borrower = models.CharField(max_length=100)
    loan_date = models.DateTimeField('date of loan')
    return_date = models.DateTimeField('date of return', null=True)
    
    def __str__(self):
        return self.recipient
