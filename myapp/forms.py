from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from myapp.models import RentDate, City, Estate
from datetime import date
import datetime
from django.forms import widgets
from airbnb.settings import DATE_INPUT_FORMATS, PAX_QUANTITY_CHOICE
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus import DateTimePickerInput


class LoginForm(AuthenticationForm):
    error_messages = {
    'invalid_login': _(
        "Usuario Inexistente"
    )} 

class FilterForm(forms.ModelForm):
    
    pax = forms.ChoiceField(choices=PAX_QUANTITY_CHOICE, label="", help_text="Cantidad de pax")
    dateFrom = forms.DateField(label="", input_formats=DATE_INPUT_FORMATS,help_text="Desde",
                                widget=DateTimePickerInput(
                                    format='%Y-%m-%d',options={'minDate':(datetime.datetime.today().strftime("%Y-%m-%d"))}).start_of('event days'))
    dateTo = forms.DateField(label="", input_formats=DATE_INPUT_FORMATS, help_text="Hasta",
                                widget=DateTimePickerInput(format='%Y-%m-%d').end_of('event days'))

    class Meta:
        model = Estate
        fields = ['city']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.all()
        self.fields['city'].label = ""
        self.fields['city'].help_text = "Ciudad"


class DetailForm(forms.ModelForm):
    user = forms.CharField(label="", max_length=30, help_text="Ingrese su nombre")
    email = forms.EmailField(label="", help_text="Ingrese su e-mail")

    class Meta:
        model = RentDate
        fields = ['dateFrom']
    
    def __init__(self, estateId, *args, **kwargs):
        super(DetailForm, self).__init__(*args, **kwargs)
        self.fields['dateFrom'] = forms.ModelMultipleChoiceField(
            queryset=RentDate.objects.filter(estate__id=estateId, reservation__isnull=True),
            label="Fechas disponibles:",
            help_text="Seleccione las fechas a reservar: CTRL+Click",
        )
        

    

