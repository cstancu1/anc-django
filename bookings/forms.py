from django import forms
from bookings.models import Location, Event, Day, Booking

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"

class LawyerForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['email', 'event', 'location', 'date', 'day', 'first_name', 'last_name',
                  'birthday', 'country', 'city', 'passport']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"