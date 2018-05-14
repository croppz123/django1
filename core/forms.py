from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django_countries.widgets import CountrySelectWidget

from core.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'birth_date', 'city', 'country', 'birth_date', 'bio']
        widgets = {'country': CountrySelectWidget(),
                   'birth_date': DatePickerInput(options={'dateFormat': 'yy-mm-dd', 'changeMonth': True,
                                                          'changeYear': True}),
                   'bio': forms.Textarea(attrs={'rows': 6, 'style': 'resize: none;',
                                                'maxlength': Profile._meta.get_field('bio').max_length})}




