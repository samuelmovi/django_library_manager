from django.test import TestCase
from django.test import Client
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template.response import TemplateResponse

from .models import Book, Location, Loan
# Create your tests here.

# MODELS


class LocationTestCase (TestCase):
    print("[#] Testing: Location Model")
    test_fields = {
        'address': 'test address',
        'room': 'test room',
        'furniture': "test furniture",
        'details': "test details",
        'username': "test user",
        'created': timezone.now(),
    }
    
    def setUp(self):
        Location.objects.create(
            address=self.test_fields['address'],
            room=self.test_fields['room'],
            furniture=self.test_fields['furniture'],
            details=self.test_fields['details'],
            created=self.test_fields['created'],
            username=self.test_fields['username'],
        )
    
    def test_content(self):
        print("[#] Testing Location model: content retrieval")
        location = Location.objects.get(address="test address")
        for field in self.test_fields:
            # print("[#] Field: {}".format(field))
            # print("\t> Instance: {}".format(location.__dict__[field]))
            # print("\t> Test value: {}".format(self.test_fields[field]))
            self.assertEqual(location.__dict__[field], self.test_fields[field])


class BookTestCase(TestCase):
    print("[#] Testing: Book Model")
    test_fields = {
        'title': 'test title',
        'author': 'test author',
        'genre': 'test genre',
        'publisher': 'test publisher',
        'isbn': 'test isbn',
        'publish_date': 'test publish_date',
        'purchase_date': 'test purchase_date',
        'location_id': None,
        'loaned': False,
        'created': timezone.now(),
        'modified': None,
        'username': 'test username',
    }
    
    def setUp(self):
        Location.objects.create(
            address='address',
            room='room',
            furniture='furniture',
            details='details',
            created=timezone.now(),
            username='username',
        )
        
        Book.objects.create(
            title=self.test_fields['title'],
            author=self.test_fields['author'],
            genre=self.test_fields['genre'],
            publisher=self.test_fields['publisher'],
            isbn=self.test_fields['isbn'],
            publish_date=self.test_fields['publish_date'],
            purchase_date=self.test_fields['purchase_date'],
            location=Location.objects.get(address='address'),
            loaned=self.test_fields['loaned'],
            created=self.test_fields['created'],
            modified=self.test_fields['modified'],
            username=self.test_fields['username'],
        )
        
    def test_content(self):
        print("[#] Testing Book model: content retrieval")
        book = Book.objects.get(title="test title")
        self.test_fields['location_id'] = Location.objects.get(address='address').id
        for field in self.test_fields:
            # print("[#] Field: {}".format(field))
            # print("\t> Instance: {}".format(book.__dict__[field]))
            # print("\t> Test value: {}".format(self.test_fields[field]))
            self.assertEqual(book.__dict__[field], self.test_fields[field])


class LoanTestCase(TestCase):
    print("[#] Testing: Loan Model")
    test_fields = {
        'book_id': '',
        'lender': 'test lender',
        'borrower': 'test borrower',
        'loan_date': timezone.now(),
        'return_date': timezone.now(),
    }
    
    def setUp(self):
        Book.objects.create(
            title='title',
            author='author',
            genre='genre',
            publisher='publisher',
            isbn='isbn',
            publish_date='publish_date',
            purchase_date='purchase_date',
            location=None,
            loaned=False,
            created=timezone.now(),
            modified=None,
            username='username',
        )
        
        Loan.objects.create(
            book=Book.objects.get(title='title'),
            lender=self.test_fields['lender'],
            borrower=self.test_fields['borrower'],
            loan_date=self.test_fields['loan_date'],
            return_date=self.test_fields['return_date'],
        )
    
    def test_content(self):
        print("[#] Testing Loan model: content retrieval")
        loan = Loan.objects.get(lender="test lender")
        self.test_fields['book_id'] = Book.objects.get(title='title').id
        for field in self.test_fields.keys():
            # print("[#] Field: {}".format(field))
            # print("\t> Instance: {}".format(loan.__dict__[field]))
            # print("\t> Test value: {}".format(self.test_fields[field]))
            self.assertEqual(loan.__dict__[field], self.test_fields[field])


# VIEWS


class LoginTestCase(TestCase):
    print("[#] Testing: Login")
    username1 = 'user1'
    password1 = 'super_secret_password'
    url = '/locations/'
    
    def setUp(self):
        print("[!] Setup")
        User.objects.create_user('user1', 'hohoho@simpson.net', 'super_secret_password')
        User.objects.create_user('user2', 'hohoho@simpson.net', 'super_secret_password')

    def test_correct_password(self):
        print("[#] Login Test: correct password")
        response = self.client.post('/login/', {
            'username': self.username1,
            'password': self.password1,
            'next': self.url,
        })
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect URL: {}".format(response.url))
        self.assertEquals(response.url, self.url)
    
    def test_wrong_password(self):
        print("[#] Test Login: wrong password")
        response = self.client.post('/login/', {
            'username': 'user2',
            'password': 'qwerqewrewrqwe',
            'next': self.url,
        })
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), TemplateResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)


class SignUpTestCase(TestCase):
    print("[#] SignUp View")
    username1 = 'user1'
    password1 = 'onmwqeoinmroiwqroiew.123'
    password2 = 'xcpobvmpoisnfdoign.532'
    username2 = 'user2'
    weak_password = '123456789'
    
    def setUp(self):
        User.objects.create_user(username=self.username1, password=self.password1)

    def test_weak_password(self):
        print("[#] SignUp Test: weak password")
        response = self.client.post('/signup', {'username': self.username2, 'password1': self.weak_password, 'password2': self.weak_password})
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponsePermanentRedirect)
        print("\t> status code: 301")
        self.assertEquals(response.status_code, 301)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/signup/')
        # check for new user instance
        print("\t> users: {}".format(User.objects.filter(username=self.username2).count()))
        users = User.objects.filter(username=self.username2).count()
        self.assertEquals(users, 0)
    
    def test_existing_username(self):
        print("[#] SignUp Test: existing user name")
        # needs to be redone using the signup page itself
        response = self.client.post('/signup', {'username': self.username1, 'password1': self.password2, 'password2': self.password2})
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponsePermanentRedirect)
        print("\t> status code: 301")
        self.assertEquals(response.status_code, 301)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/signup/')
        print("\t> users: {}".format(User.objects.filter(username=self.username1).count()))
        """
        users = User.objects.filter(username=self.username1).count()
        self.assertEquals(users, 1)
        with self.assertRaises(IntegrityError) as context:
            User.objects.create_user(username=self.username1, password=self.password2)
        self.assertEqual(IntegrityError, type(context.exception))
        """
        
    def test_good_signup(self):
        print("[#] SignUp Test: good signup")
        c = Client()
        response = c.post('/signup/', {'username': self.username2, 'password1': self.password2, 'password2': self.password2})
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect path: {}".format(response.url))
        self.assertEquals('/', response.url)
        # check for new user instance
        print("\t> all users: {}".format(User.objects.all().count()))
        users = User.objects.filter(username=self.username2).count()
        self.assertEquals(users, 1)
        print('\t> content: {}'.format(response.content))
        self.assertEquals(b'', response.content)


class BooksTestCase(TestCase):
    print("[#] Books View")
    username1 = 'user1'
    password1 = 'super_secret_password'
    string = 'qwerQWR$£RqewfrQ3r'

    def setUp(self):
        User.objects.create_user(username=self.username1, password=self.password1)
        self.client.login(username=self.username1, password=self.password1)
        Book.objects.create(
            title=self.string,
            author=self.string,
            genre=self.string,
            publisher=self.string,
            isbn=self.string,
            publish_date=self.string,
            purchase_date=self.string,
            location=None,
            loaned=False,
            created=timezone.now(),
            modified=timezone.now(),
            username=self.username1,
        )
    
    def test_login_required(self):
        c = Client()
        response = c.get('/books/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/login/?next=/books/')
        
    def test_get_page(self):
        print("[#] Books View: info retrieval")
        print("\t> Adding book to db...")
        response = self.client.get("/books/")
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), TemplateResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)
        print("\t> book info in content...")
        content = response.content.decode()
        self.assertEquals(content.count(self.string), 6)


class NewBookTestCase(TestCase):
    print("[#] NewBook View")
    username1 = 'user1'
    password1 = 'super_secret_password'
    string = "DSfgDSFvFDSv"
    new_book = {
        "title": string,
        "author": string,
        "genre": string,
        "publisher": string,
        "isbn": string,
        "publish_date": string,
        "purchase_date": string,
    }
    
    def setUp(self):
        User.objects.create_user(username=self.username1, password=self.password1)
        self.client.login(username=self.username1, password=self.password1)
    
    def test_login_required(self):
        c = Client()
        response = c.get('/books/new/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/login/?next=/books/new/')
    
    def test_get_page(self):
        print("[#] New Book: page retrieval")
        response = self.client.get('/books/new/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)
    
    def test_post_new_book(self):
        print("[#] New Book: posting new book")
        response = self.client.post('/books/new/', {
                                                "title": self.string,
                                                "author": self.string,
                                                "genre": self.string,
                                                "publisher": self.string,
                                                "isbn": self.string,
                                                "publish_date": self.string,
                                                "purchase_date": self.string,
                                            })
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/books/')
        count = Book.objects.filter(title=self.string).count()
        self.assertEquals(count, 1)
     

class BookInfoTestCase(TestCase):
    print("[#] BookInfo View")
    username1 = 'user1'
    password1 = 'super_secret_password'
    string = "jdfgjJdfgJfdGHDfhC"
    string2 = "qweFC dsaCCAQesdc"
    book_id = 0
    
    def setUp(self):
        User.objects.create_user(username=self.username1, password=self.password1)
        self.client.login(username=self.username1, password=self.password1)
        Book.objects.create(
            title=self.string,
            author=self.string,
            genre=self.string,
            publisher=self.string,
            isbn=self.string,
            publish_date=self.string,
            purchase_date=self.string,
            location=None,
            loaned=False,
            created=timezone.now(),
            modified=timezone.now(),
            username=self.username1,
        )
        self.book_id = Book.objects.get(title=self.string).id

    def test_login_required(self):
        c = Client()
        response = c.get('/books/0/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/login/?next=/books/0/')

    def test_get_page(self):
        response = self.client.get('/books/{}/'.format(self.book_id))
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)

    def test_get_book_info(self):
        response = self.client.get('/books/{}/'.format(self.book_id))
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)
        print("\t> modified book info in content...")
        content = response.content.decode()
        self.assertEquals(content.count(self.string), 7)
    
    def test_modify_book(self):
        response = self.client.post('/books/{}/'.format(self.book_id), {
            "bookID": self.book_id,
            "title": self.string2,
            "author": self.string2,
            "genre": self.string2,
            "publisher": self.string2,
            "isbn": self.string2,
            "publish_date": self.string2,
            "purchase_date": self.string2,
            "action": "modify",
        })
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/books/')
        response = self.client.get(response.url)
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), TemplateResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)
        print("\t> modified book info in content...")
        content = response.content.decode()
        self.assertEquals(content.count(self.string2), 6)

    def test_delete_book(self):
        response = self.client.post('/books/{}/'.format(self.book_id),
                                    {"bookID": self.book_id, "action": "delete"})
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/books/')
        with self.assertRaises(Exception) as context:
            Book.objects.get(title=self.string)
        self.assertEqual(Book.DoesNotExist, type(context.exception))


"""
class ModifyBookTestCase(TestCase):
    print("[#] ModifyBook View")
    username1 = 'user1'
    password1 = 'super_secret_password'
    string = "jdfgjJdfgJfdGHDfhC"
    string2 = "qweFC dsaCCAQesdc"
    
    def setUp(self):
        User.objects.create_user(username=self.username1, password=self.password1)
        self.client.login(username=self.username1, password=self.password1)
        Book.objects.create(
            title=self.string,
            author=self.string,
            genre=self.string,
            publisher=self.string,
            isbn=self.string,
            publish_date=self.string,
            purchase_date=self.string,
            location=None,
            loaned=False,
            created=timezone.now(),
            modified=timezone.now(),
            username=self.username1,
        )
    
    def test_login_required(self):
        c = Client()
        response = c.get('/books/modify/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/login/?next=/books/modify/')
    
    def test_get_page(self):
        response = self.client.get('/books/modify/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)
    
    def test_get_book_info(self):
        book_id = Book.objects.get(title=self.string).id
        response = self.client.post('/books/modify/', {'bookID': book_id})
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)
        print("\t> modified book info in content...")
        content = response.content.decode()
        self.assertEquals(content.count(self.string), 7)
        
    def test_modify_book(self):
        book_id = Book.objects.get(title=self.string).id
        response = self.client.post('/books/modify/{}/'.format(book_id), {
            "bookID": book_id,
            "title": self.string2,
            "author": self.string2,
            "genre": self.string2,
            "publisher": self.string2,
            "isbn": self.string2,
            "publish_date": self.string2,
            "purchase_date": self.string2,
        })
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/books/')
        response = self.client.get(response.url)
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), TemplateResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)
        print("\t> modified book info in content...")
        content = response.content.decode()
        self.assertEquals(content.count(self.string2), 7)


class DeleteBookTestCase(TestCase):
    print("[#] DeleteBook View")
    username1 = 'user1'
    password1 = 'super_secret_password'
    string = "WQER£frFwefFwe23"
    
    def setUp(self):
        User.objects.create_user(username=self.username1, password=self.password1)
        self.client.login(username=self.username1, password=self.password1)
        Book.objects.create(
            title=self.string,
            author=self.string,
            genre=self.string,
            publisher=self.string,
            isbn=self.string,
            publish_date=self.string,
            purchase_date=self.string,
            location=None,
            loaned=False,
            created=timezone.now(),
            modified=timezone.now(),
            username=self.username1,
        )
    
    def test_login_required(self):
        c = Client()
        response = c.get('/books/delete/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/login/?next=/books/delete/')

    def test_get_page(self):
        response = self.client.get('/books/delete/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)
    
    def test_delete_book(self):
        response = self.client.post('/books/delete/',
                                    {'bookID': Book.objects.get(title=self.string).id})
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/books/')
        with self.assertRaises(Exception) as context:
            Book.objects.get(title=self.string)
        self.assertEqual(Book.DoesNotExist, type(context.exception))

"""


class LocationsViewTestCase(TestCase):
    print("[#] Locations View")
    username1 = 'user1'
    password1 = 'super_secret_password'
    string = "YUGFHJgfhjfghjFHj"
    
    def setUp(self):
        User.objects.create_user(username=self.username1, password=self.password1)
        self.client.login(username=self.username1, password=self.password1)
        Location.objects.create(
            address=self.string,
            room=self.string,
            furniture=self.string,
            details=self.string,
            created=timezone.now(),
            username=self.username1,
        )
    
    def test_login_required(self):
        c = Client()
        response = c.get('/locations/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/login/?next=/locations/')

    def test_get_page(self):
        response = self.client.get('/locations/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), TemplateResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)
        print("\t> location info in content...")
        content = response.content.decode()
        self.assertEquals(content.count(self.string), 4)
    

class NewLocationView(TestCase):
    print("[#] NewLocation View")
    username1 = 'user1'
    password1 = 'super_secret_password'
    string = "56HTYjtyJjghj"
    
    def setUp(self):
        User.objects.create_user(username=self.username1, password=self.password1)
        self.client.login(username=self.username1, password=self.password1)
    
    def test_login_required(self):
        c = Client()
        response = c.get('/locations/new/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/login/?next=/locations/new/')

    def test_get_page(self):
        response = self.client.get('/locations/new/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)

    def test_post_new_location(self):
        response = self.client.post('/locations/new/',
                                    {'address': self.string,
                                     'room': self.string,
                                     'furniture': self.string,
                                     'details': self.string})
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/locations/')
        count = Location.objects.filter(address=self.string).count()
        self.assertEquals(count, 1)


class LocationInfoTestCase(TestCase):
    print("[#] LocationInfo View")
    username1 = 'user1'
    password1 = 'super_secret_password'
    string = "NMJuyMuMjyNhy"
    string2 = "juny76 U76uN&^"
    location_id = 0

    def setUp(self):
        User.objects.create_user(username=self.username1, password=self.password1)
        self.client.login(username=self.username1, password=self.password1)
        Location.objects.create(
            address=self.string,
            room=self.string,
            furniture=self.string,
            details=self.string,
            created=timezone.now(),
            username=self.username1,
        )
        self.location_id = Location.objects.get(details=self.string).id

    def test_login_required(self):
        c = Client()
        response = c.get('/locations/{}/'.format(self.location_id))
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/login/?next=/locations/{}/'.format(self.location_id))

    def test_get_page(self):
        response = self.client.get('/locations/{}/'.format(self.location_id).format(self.location_id))
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)
        content = response.content.decode()
        self.assertEquals(content.count(self.string), 4)
    
    def test_modify_location(self):
        response = self.client.post('/locations/{}/'.format(self.location_id), {
            "locationID": self.location_id,
            "address": self.string2,
            "room": self.string2,
            "furniture": self.string2,
            "details": self.string2,
            "action": "modify",
        })
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/locations')
        response = self.client.get(response.url)
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponsePermanentRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 301)
        print("\t> modified book info in content...")
        content = response.content.decode()
        self.assertEquals(content.count(self.string2), 4)

    def test_delete_location(self):
        response = self.client.post('/locations/{}/'.format(self.location_id),
                                    {'locationID': Location.objects.get(address=self.string).id, "action": "delete"})
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/locations')
        with self.assertRaises(Exception) as context:
            Location.objects.get(address=self.string)
        self.assertEqual(Location.DoesNotExist, type(context.exception))


"""
class DeleteLocationTestCase(TestCase):
    print("[#] DeleteLocation View")
    username1 = 'user1'
    password1 = 'super_secret_password'
    string = "NMJuyMuMjyNhy"
    
    def setUp(self):
        User.objects.create_user(username=self.username1, password=self.password1)
        self.client.login(username=self.username1, password=self.password1)
        Location.objects.create(
            address=self.string,
            room=self.string,
            furniture=self.string,
            details=self.string,
            created=timezone.now(),
            username=self.username1,
        )
    
    def test_login_required(self):
        c = Client()
        response = c.get('/locations/delete/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/login/?next=/locations/delete/')

    def test_get_page(self):
        response = self.client.get('/locations/delete/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)

    def test_delete_location(self):
        response = self.client.post('/locations/delete/',
                                    {'locationID': Location.objects.get(address=self.string).id})
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/locations/')
        with self.assertRaises(Exception) as context:
            Location.objects.get(address=self.string)
        self.assertEqual(Location.DoesNotExist, type(context.exception))
"""


class LoansViewTestCase(TestCase):
    print("[#] Loans View")
    username1 = 'user1'
    password1 = 'super_secret_password'
    string = "vXcvxVxCcCvB"
    
    def setUp(self):
        User.objects.create_user(username=self.username1, password=self.password1)
        self.client.login(username=self.username1, password=self.password1)
        Book.objects.create(
            title=self.string,
            author=self.string,
            genre=self.string,
            publisher=self.string,
            isbn=self.string,
            publish_date=self.string,
            purchase_date=self.string,
            location=None,
            loaned=False,
            created=timezone.now(),
            modified=timezone.now(),
            username=self.username1,
        )
        Loan.objects.create(
            book=Book.objects.get(title=self.string),
            lender=self.string,
            borrower=self.string,
            loan_date=timezone.now(),
        )
    
    def test_login_required(self):
        c = Client()
        response = c.get('/loans/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/login/?next=/loans/')

    def test_get_page(self):
        response = self.client.get('/loans/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), TemplateResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)
        print("\t> loan info in content...")
        content = response.content.decode()
        self.assertEquals(content.count(self.string), 1)


class LoanBookTestCase(TestCase):
    print("[#] LoanBook View")
    username1 = 'user1'
    password1 = 'super_secret_password'
    string = "akjdofkadsFadsFt"
    
    def setUp(self):
        User.objects.create_user(username=self.username1, password=self.password1)
        self.client.login(username=self.username1, password=self.password1)
        Book.objects.create(
            title=self.string,
            author=self.string,
            genre=self.string,
            publisher=self.string,
            isbn=self.string,
            publish_date=self.string,
            purchase_date=self.string,
            location=None,
            loaned=False,
            created=timezone.now(),
            modified=timezone.now(),
            username=self.username1,
        )
    
    def test_login_required(self):
        c = Client()
        response = c.get('/loans/loan/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/login/?next=/loans/loan/')
    
    def test_get_page(self):
        response = self.client.get('/loans/loan/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)
        print("\t> loan info in content...")
        content = response.content.decode()
        self.assertEquals(content.count(self.string), 5)
    
    def test_loan_book(self):
        book_id = Book.objects.get(title=self.string).id
        response = self.client.post('/loans/loan/', {'bookID': book_id, 'recipient': self.string})
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/loans/')
        count = Loan.objects.all().count()
        self.assertEquals(count, 1)


class ReturnBookTestCase(TestCase):
    print("[#] ReturnBook View")
    username1 = 'user1'
    password1 = 'super_secret_password'
    string = "okpoaedfaDSF"
    
    def setUp(self):
        User.objects.create_user(username=self.username1, password=self.password1)
        self.client.login(username=self.username1, password=self.password1)
        Book.objects.create(
            title=self.string,
            author=self.string,
            genre=self.string,
            publisher=self.string,
            isbn=self.string,
            publish_date=self.string,
            purchase_date=self.string,
            location=None,
            loaned=True,
            created=timezone.now(),
            modified=timezone.now(),
            username=self.username1,
        )
        Loan.objects.create(
            book=Book.objects.get(title=self.string),
            lender=self.username1,
            borrower=self.string,
            loan_date=timezone.now(),
            return_date=None,
        )
        
    def test_login_required(self):
        c = Client()
        response = c.get('/loans/return/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/login/?next=/loans/return/')

    def test_get_page(self):
        response = self.client.get('/loans/return/')
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponse)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 200)
    
    def test_return_book(self):
        print("[#] post return book")
        loan_id = Loan.objects.get(borrower=self.string).id
        response = self.client.post('/loans/return/', {'loanID': loan_id})
        print("\t> response type: {}".format(type(response)))
        self.assertEquals(type(response), HttpResponseRedirect)
        print("\t> status code: {}".format(response.status_code))
        self.assertEquals(response.status_code, 302)
        print("\t> redirect chain: {}".format(response.url))
        self.assertEquals(response.url, '/loans/')
        book = Book.objects.get(title=self.string)
        self.assertEquals(book.loaned, False)
        count = Loan.objects.filter(return_date=None).count()
        self.assertEqual(count, 0)

