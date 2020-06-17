from django.urls import path, re_path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view() , name='book-detail'),
    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    re_path(r'^mybooks/$', views.LoanedBookByUserListView.as_view(), name='my-borrowed'),
    re_path(r'^borrowed-books/$', views.StaffBorrowedListView.as_view(), name='all-borrowed'),
    re_path(r'^ava-books/$', views.StaffAvaListView.as_view(), name='ava-books'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]



urlpatterns += [  
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
]

urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
    path('bookinstance/<uuid:pk>/borrownew/', views.BookBorrowNew.as_view(), name='book_borrow_new'),
]
