from django.contrib import admin

from .models import Author, Book, BookInstance, Genre, Language



#admin.site.register(models.Book)
#admin.site.register(models.Author)


admin.site.register(Genre)
#admin.site.register(models.BookInstance)
admin.site.register(Language)

class BookInline(admin.StackedInline):
    model = Book
    raw_id_fields = ('language',)
    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
    


admin.site.register(Author, AuthorAdmin)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    min_num = 3
    

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    
    fieldsets = (
        (None, {
            'fields': ('title','author', 'summary')
        }),
        ('Category',{
            'fields': ('genre', 'language')
        }),
    )
    inlines = [BookInstanceInline]

    
    
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book','imprint','id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
