from django import forms
from django.utils import timezone
from .models import Auction


class AuctionForm(forms.ModelForm):

    class Meta:
        model = Auction
        fields = ['item_name','description','category','image','starting_price','minimum_bid_increment','start_datetime','end_datetime',]


    def clean_starting_price(self):
        price = self.cleaned_data['starting_price']

        if price <= 0:
            raise forms.ValidationError('Starting price must be greater than 0.')
        return price

    def clean_minimum_bid_increment(self):
        increment = self.cleaned_data['minimum_bid_increment']
        if increment <= 0:
            raise forms.ValidationError('Minimum bid increment must be greater than 0.')

        return increment

    def clean(self):
        cleaned_data = super().clean()

        start_datetime = cleaned_data.get('start_datetime')
        end_datetime = cleaned_data.get('end_datetime')

        if start_datetime:
            if timezone.is_naive(start_datetime):
                start_datetime = timezone.make_aware(start_datetime)

            if start_datetime <= timezone.now():
                self.add_error('start_datetime','Auction start time must be in the future.')

        if start_datetime and end_datetime:

            if timezone.is_naive(end_datetime):
                end_datetime = timezone.make_aware(end_datetime)

            if end_datetime <= start_datetime:
                self.add_error('end_datetime','Auction end time must be after start time.')

        return cleaned_data



    