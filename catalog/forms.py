import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Enter New Due Date Max 4 week (default:3)')


    def clean_renewal_date(self):

        data = self.cleaned_data['renewal_date']

        #check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid Date - renewal in past '))

        #check if a date is in the future
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal in the future'))


        #Remember to always return the cleaned data.
        return data




from catalog.models import BookInstance

class RenewBookModelForm(forms.ModelForm):

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - Very Old'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid Date - Out of range'))

        return data

    
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'deb_back': _('Enter a Renew Date')}
        help_text = {'due_back': _('Enter a new date between 4 weeks')}
