from django.forms import ModelForm
from django_countries.widgets import CountrySelectWidget
from .models import Address


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'complement', 'country', 'state', 'city', 'zip']
        widgets = {'country': CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            classes = self.fields[field].widget.attrs.get("class")
            classes = " form-control"
            self.fields[field].widget.attrs.update({
            'class': classes
            })
