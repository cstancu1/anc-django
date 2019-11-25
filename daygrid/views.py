from django.shortcuts import render
from bookings.models import Booking, Location, Event
import json
from django.core import serializers

def main(request):
    events = Event.objects.all()
    locations = Location.objects.all()
    locations_json = []
    events_json = []
    for location in locations:
        temp_dict = {}
        temp_dict['name'] = location.name
        temp_dict['details'] = location.details
        locations_json.append(temp_dict)

    for event in events:
        temp_dict = {}
        temp_dict['name'] = event.name
        temp_dict['details'] = event.details
        if event.is_lawyer == False:
            temp_dict['is_lawyer'] = 'false' 
        else:
            temp_dict['is_lawyer'] = 'true' 
        temp_dict['location'] = event.location.name
        temp_dict['address'] = event.address
        events_json.append(temp_dict)
        
    context={}
    context['locations'] = locations_json
    context['events'] = events_json
    print(context)
    return render(request, template_name='daygrid/index.html', context=context)

def get_events(request):
    location=request.args.get('location')
    events = Event.objects.filter(location=location)
    print('events')
    return events