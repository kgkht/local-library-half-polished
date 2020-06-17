from django.shortcuts import render, get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre

# Create your views here.
def index(request):
    """ For Home Page """
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_ava = BookInstance.objects.filter(status__exact='a').count()
    num_genre = Genre.objects.all().count()
    num_authors = Author.objects.all().count()

    #add number of visitors using sessions
    num_visitors = request.session.get('num_visitors', 0)
    request.session['num_visitors'] = num_visitors + 1
    

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_ins_ava': num_instances_ava,
        'num_genre': num_genre,
        'num_authors': num_authors,
        'num_visitors': num_visitors,
    }
    return render(request, 'catalog/home.html', context)


from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

    def get_queryset(self):
        self.context = Book.objects.all()[:5]
        return self.context

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        context['another_list'] = Book.objects.filter(title__icontains='Noon')
        return context


class AuthorListView(generic.ListView):
    model = Author
    
    

class BookDetailView(generic.DetailView):
    model = Book



class AuthorDetailView(generic.DetailView):
    model = Author



from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    



from django.contrib.auth.mixins import PermissionRequiredMixin
class StaffBorrowedListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_borrowed_book.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')



class StaffAvaListView(PermissionRequiredMixin, generic.ListView):

    permission_required = 'catalog.can_mark_returned'

    model = BookInstance
    template_name = 'catalog/bookinstance_ava_book.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='a').order_by('due_back')

    

import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from catalog.forms import RenewBookModelForm as RenewBookForm


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            return HttpResponseRedirect(reverse('catalog:all-borrowed'))


    else:
        proposed_renewal_date = datetime.timedelta(weeks=3) + datetime.date.today()
        form = RenewBookForm(initial={'due_back': proposed_renewal_date})


    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)




from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2019'}


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('catalog:authors')



class BookCreate(CreateView):
    model = Book
    fields = ['title', 'summary', 'isbn']


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('catalog:books')



class BookBorrowNew(UpdateView):
    model = BookInstance
    fields = '__all__'


        
from django.contrib.auth.models import User
    
class ProfileUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username','email' ]
    success_url = reverse_lazy('catalog:index')

