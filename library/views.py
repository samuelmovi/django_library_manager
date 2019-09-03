from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.views import generic
from django.views import View
from django.middleware.csrf import CsrfViewMiddleware
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
# Create your views here.


from .models import *

# Create your views here.
book_table_headers = {
    'title': _('Title'),
    'author': _('Author'),
    'genre': _('Genre'),
    'publisher': _('Publisher'),
    'isbn': _('ISBN'),
    'publish_date': _('Publish date'),
    'purchase_date': _('Purchase date'),
    'loaned': _('On Loan')
}
location_table_headers = {
    'address': _('Address'),
    'room': _('Room'),
    'furniture': _('Furniture'),
    'details': _('Details'),
}
loan_table_headers = {
    'book': _('Book'),
    'borrower': _('Borrower'),
    'loan_date': _('Loan Date'),
    'return_date': _('Return Date'),
}


def bad_data(request):
    return render(request, 'library/bad_data.html')


class SignUp(View):
    
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'library/signup.html', {'form': form})
    
    def post(self, request):
        try:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'library/signup.html', {'form': form})
        except Exception:
            return redirect('/bad_data/')


@login_required(login_url='/login/')
def log_me_out(request):
    try:
        logout(request)
        return redirect('/')
    except Exception:
        return redirect('/bad_data/')


@login_required(login_url='/login/')
def home(request):
    try:
        page_title = _('Please Login to Your Library Manager')
        # header = _('Welcome to your libary {}'.format(request.user.username))
        books = Book.objects.filter(username=request.user.username).count()
        loans = Book.objects.filter(username=request.user.username, loaned=True).count()
        context = {
            'page_title': page_title,
            # 'my_header': header,
            'books': books,
            'loans': loans,
        }
        return render(request, 'library/home.html', context)
    except Exception:
        return redirect('/bad_data/')


class BooksView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    template_name = 'library/show_books.html'
    title = _("All Books")
    bottom_bar = [
        {'href': '/books/new/', 'text': _('New')},
        {'href': '/books/modify/', 'text': _('Modify')},
        {'href': '/books/delete/', 'text': _('Delete')},
    ]
    
    def get_queryset(self):
        pass
    
    def get_context_data(self, *, object_list=None, **kwargs):
        all_books = Book.objects.order_by('author')
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.title
        #  context['my_header'] = header,
        context['table_headers'] = book_table_headers
        context['books'] = all_books
        # context['bottom_bar'] = self.bottom_bar
        return context


class BookInfo(LoginRequiredMixin, View):
    login_url = '/login/'
    model_fields = [
        'title', 'author', 'genre', 'publisher',
        'isbn', 'publish_date', 'purchase_date', 'location']
    
    def get(self, request, book_id, **kwargs):
        try:
            book = Book.objects.get(pk=book_id)
            # prepare location drop-down data
            all_locations = Location.objects.order_by('address')
            my_locations = []
            for location in all_locations:
                value = location.id
                text = location.address + ' - ' + location.room + ' - ' + location.furniture + ' - ' + location.details
                data = {'value': value, 'text': text}
                my_locations.append(data)
            # set response's context
            context = {
                'book': book,
                'all_locations': my_locations,
                'action': 'modify',
            }
            return render(request, 'library/book_info.html', context)
        except Exception as e:
            print("[!] Error processing request: {}".format(e))
            return redirect('/bad_data/')

    def post(self, request, book_id):
        # check csrf
        request.csrf_processing_done = False
        reason = CsrfViewMiddleware().process_view(request, None, (), {})
        if reason is not None:
            return reason
        # for k, v in request.POST.items():
        #    print('\t> {}: {}'.format(k, v))
        # SELECT ACTION
        if request.POST.get('action') == 'modify':
            book = Book.objects.get(pk=book_id)
            for field in self.model_fields:
                book.__dict__[field] = request.POST.get(field, None)
            # update modification date field
            book.modified = timezone.now()
            book.save()
        elif request.POST.get('action') == 'delete':
            # deleting db model entry
            Book.objects.filter(pk=book_id).delete()
        else:
            return redirect('/bad_data/')
        return redirect('/books/')


class NewBook(LoginRequiredMixin, View):
    login_url = '/login/'
    model_fields = [
        'title', 'author', 'genre', 'publisher',
        'isbn', 'publish_date', 'purchase_date', 'location']
    
    def get(self, request):
        try:
            all_locations = Location.objects.order_by('id')
            my_locations = []
            for location in all_locations:
                value = location.id
                text = location.address + ' - ' + location.room + ' - ' + location.furniture + ' - ' + location.details
                data = {'value': value, 'text': text}
                my_locations.append(data)
            context = {
                # 'my_header': header,
                'all_locations': my_locations,
                'action': 'new',
            }
            return render(request, 'library/book_info.html', context)
        except Exception:
            return redirect('/bad_data/')
    
    def post(self, request):
        try:
            # check csrf
            request.csrf_processing_done = False
            reason = CsrfViewMiddleware().process_view(request, None, (), {})
            if reason is not None:
                return reason
            # set user input data
            book = Book()
            print("[#] New Book:")
            for field in self.model_fields:
                book.__dict__[field] = request.POST.get(field, '')
                print("\t> {}: {}".format(field, book.__dict__[field]))
            # set system data
            book.loaned = False
            book.username = request.user.username
            book.created = timezone.now()
            # add model to db
            book.save()
            return redirect('/books/')
        except Exception:
            return redirect('/bad_data/')


class ModifyBook(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        try:
            title = _("Choose Book to Modify")
            all_books = Book.objects.filter(username=request.user.username).order_by('id')
            context = {
                'action': 'modify',
                'page_title': title,
                # 'my_header': header,
                'books': all_books,
                'table_headers': book_table_headers,
                'button_text': title,
                'link': '/library/books/modify/'
            }
            return render(request, 'library/choose_book.html', context)
        except Exception:
            return redirect('/bad_data/')
    
    def post(self, request):
        try:
            # check csrf
            request.csrf_processing_done = False
            reason = CsrfViewMiddleware().process_view(request, None, (), {})
            if reason is not None:
                return reason
            # get object from bookID
            book = Book.objects.get(pk=request.POST['bookID'])
            for k, v in request.POST.items():
                print('\t> {}: {}'.format(k, v))
            # prepare location drop-down data
            all_locations = Location.objects.order_by('address')
            my_locations = []
            for location in all_locations:
                value = location.id
                text = location.address + ' - ' + location.room + ' - ' + location.furniture + ' - ' + location.details
                data = {'value': value, 'text': text}
                my_locations.append(data)
            # set response's context
            context = {
                'book': book,
                'all_locations': my_locations,
                'action': 'modify',
            }
            return render(request, 'library/book_info.html', context)
        except Exception:
            return redirect('/bad_data/')


@login_required(login_url='/login/')
def book_modifier(request, **kwargs):
    try:
        if request.method == 'POST':
            model_fields = [
                'title', 'author', 'genre', 'publisher',
                'isbn', 'publish_date', 'purchase_date', 'location']
            # check csrf
            request.csrf_processing_done = False
            reason = CsrfViewMiddleware().process_view(request, None, (), {})
            if reason is not None:
                return reason
            # get requested data
            book = Book.objects.get(pk=request.POST['bookID'])
            for field in model_fields:
                book.__dict__[field] = request.POST.get(field, None)
            # update modification date field
            book.modified = timezone.now()
            book.save()
            return redirect('/books/')
        else:
            # send to bad data page
            raise Http404(_("You are using the wrong type of method: {}".format(request.method)))
    except Exception:
        return redirect('/bad_data/')


class DeleteBook(LoginRequiredMixin, View):
    login_url = '/login/'
    title = _("Choose Book to Delete")
    
    def get(self, request):
        try:
            all_books = Book.objects.filter(username=request.user.username).order_by('id')
            context = {
                'action': 'delete',
                'page_title': self.title,
                # 'my_header': header,
                'books': all_books,
                'table_headers': book_table_headers,
                'button_text': self.title,
                'link': '/library/books/delete/',
            }
            return render(request, 'library/choose_book.html', context)
        except Exception:
            return redirect('/bad_data/')
    
    def post(self, request):
        try:
            # check csrf
            request.csrf_processing_done = False
            reason = CsrfViewMiddleware().process_view(request, None, (), {})
            if reason is not None:
                return reason
            # deleting db model entry
            Book.objects.filter(pk=request.POST['bookID']).delete()
            return redirect('/books/')
        except Exception:
            return redirect('/bad_data/')


class LocationsView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    template_name = 'library/show_locations.html'
    title = _("All Locations")
    bottombar_links = [
        {'href': '/locations/new/', 'text': _('New')},
        {'href': '/locations/delete/', 'text': _('Delete')},
    ]
    
    def get_queryset(self):
        pass
    
    def get_context_data(self, *, object_list=None, **kwargs):
        all_locations = Location.objects.order_by('address')
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.title
        # context['my_header'] = header,
        context['bottom_bar'] = self.bottombar_links
        context['table_headers'] = location_table_headers
        context['locations'] = all_locations
        return context


class NewLocation(LoginRequiredMixin, View):
    login_url = '/login/'
    location_fields = ['address', 'room', 'furniture', 'details']
    
    def get(self, request):
        try:
            context = {
                # 'my_header': header,
                'action': 'new',
            }
            return render(request, 'library/location_info.html', context)
        except Exception:
            return redirect('/bad_data/')
    
    def post(self, request):
        try:
            # check csrf
            request.csrf_processing_done = False
            reason = CsrfViewMiddleware().process_view(request, None, (), {})
            if reason is not None:
                return reason
            # new model instance
            location = Location()
            # add user input
            for field in self.location_fields:
                location.__dict__[field] = request.POST.get(field, '')
            # add system data
            location.created = timezone.now()
            # add instance to db
            location.save()
            return redirect('/locations/')
        except Exception:
            return redirect('/bad_data/')


class DeleteLocation(LoginRequiredMixin, View):
    login_url = '/login/'
    title = _("Choose Location to Delete")
    
    def get(self, request):
        try:
            all_location = Location.objects.order_by('id')
            context = {
                'action': 'delete',
                'page_title': self.title,
                # 'my_header': header,
                'locations': all_location,
                'table_headers': location_table_headers,
                'button_text': self.title,
            }
            return render(request, 'library/choose_location.html', context)
        except Exception:
            return redirect('/bad_data/')
    
    def post(self, request):
        try:
            # check csrf
            request.csrf_processing_done = False
            reason = CsrfViewMiddleware().process_view(request, None, (), {})
            if reason is not None:
                return reason
            # deleting db model entry
            Location.objects.filter(pk=request.POST['locationID']).delete()
            return redirect('/locations/')
        except Exception:
            return redirect('/bad_data/')


class LoansView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    template_name = 'library/show_loans.html'
    title = _("All Loans")
    bottom_bar = [
        {'href': '/loans/loan/', 'text': _('Loan')},
        {'href': '/loans/return/', 'text': _('Return')},
    ]
    
    def get_queryset(self):
        pass
    
    def get_context_data(self, *, object_list=None, **kwargs):
        all_loans = Loan.objects.order_by('loan_date')
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.title
        # context['my_header'] = header,
        context['bottom_bar'] = self.bottom_bar
        context['table_headers'] = loan_table_headers
        context['loans'] = all_loans
        return context


class LoanBook(LoginRequiredMixin, View):
    login_url = '/login/'
    page_title = _("Choose Book to Loan and Recipient")
    button_text = _('Loan Book')
    
    def get(self, request):
        try:
            all_books = Book.objects.filter(username=request.user.username, loaned=False).order_by('id')
            context = {
                'action': 'loan',
                'page_title': self.page_title,
                # 'my_header': header,
                'books': all_books,
                'table_headers': book_table_headers,
                'button_text': self.button_text,
                'link': '/library/books/modify/'
            }
            return render(request, 'library/choose_book.html', context)
        except Exception:
            return redirect('/bad_data/')
    
    def post(self, request):
        try:
            # check csrf
            request.csrf_processing_done = False
            reason = CsrfViewMiddleware().process_view(request, None, (), {})
            if reason is not None:
                return reason
            # check book is not already loaned
            # set book as loaned
            book = Book.objects.get(pk=request.POST['bookID'])
            if book.loaned is True:
                return redirect('/loans/')
            book.loaned = True
            book.save()
            # create new loan
            loan = Loan()
            loan.recipient = request.POST['recipient']
            loan.book_id = request.POST['bookID']
            loan.loan_date = timezone.now()
            loan.save()
            return redirect('/loans/')
        except Exception:
            return redirect('/bad_data/')


class ReturnBook(LoginRequiredMixin, View):
    login_url = '/login/'
    page_title = _("Choose Book to Return")
    
    def get(self, request):
        try:
            all_loans = Loan.objects.filter(return_date=None).order_by('loan_date')
            context = {
                'page_title': self.page_title,
                # 'my_header': header,
                'loans': all_loans,
                'table_headers': loan_table_headers,
                'button_text': self.page_title,
            }
            return render(request, 'library/choose_loan.html', context)
        except Exception:
            return redirect('/bad_data/')
    
    def post(self, request):
        try:
            # check csrf
            request.csrf_processing_done = False
            reason = CsrfViewMiddleware().process_view(request, None, (), {})
            if reason is not None:
                return reason
            # set return date
            loan = Loan.objects.get(pk=request.POST['loanID'])
            loan.return_date = timezone.now()
            # set book as returned
            book = Book.objects.get(pk=loan.book_id)
            if book.loaned is False:
                return redirect('/bad_data/')
            else:
                book.loaned = False
            book.save()
            loan.save()
            return redirect('/loans/')
        except Exception:
            return redirect('/bad_data/')
