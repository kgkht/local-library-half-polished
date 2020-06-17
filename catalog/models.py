from django.db import models
from django.urls import reverse

# Create your models here.

class Genre(models.Model):
    """ Model represent a book gener """
    name = models.CharField(max_length=200, help_text='Enter a book genre')

    def __str__(self):
        return self.name


class Book(models.Model):
    """ Model represent a book (but not a copy of a specify copy of a book)."""
    title = models.CharField('Book Title', max_length=250)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a desb of a book.')

    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character')

    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book.')

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):

        return self.title


    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[str(self.id)])

    def get_abs_url(self):
        return reverse('catalog:book-detail', args=[str(self.id)])


    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    
    def short_title(self):
        return self.title[:25]


import uuid
from django.contrib.auth.models import User
from datetime import date

class BookInstance(models.Model):
    """ Model represent a specify copy of a book."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this book')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200, help_text='Version Details')
    
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering=['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)


    def __str__(self):
        """ String for representing the model Object"""
        return '{0} ({1})'.format(self.id, self.book.title)


    def display_book(self):
        return '{0} ({1})'.format(self.book.title, self.book.author)


    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[str(self.book.id)])


    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    

class Author(models.Model):
    """ MODEL represent an author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died Date', null=True, blank=True)

    
    class Meta:
        ordering = ['last_name', 'first_name']



    def get_abs_url(self):
        return reverse('catalog:author-detail', args=[str(self.id)])

    
    def get_absolute_url(self):
        return reverse('catalog:author-detail', args=[str(self.id)])
    
    
    def __str__(self):
        return '{0} {1}'.format(self.last_name, self.first_name)


    

class Language(models.Model):
    """ Model represent with a book's language"""
    name = models.CharField(max_length=100, help_text='Enter a book of language')

    def __str__(self):
        return self.name



