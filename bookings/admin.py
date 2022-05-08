from django.contrib import admin
from bookings.models import Location, Event, Day, Booking
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from datetime import date, timedelta


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'address', 'last_date')

class BookingAdmin(admin.ModelAdmin):
    ordering = ['created', 'first_name', 'last_name', 'country', 'is_lawyer', 'date', 'email']
    search_fields = ['email','date','passport', 'first_name','last_name']
    list_display = ('location', 'event', 'date', 'first_name', 'last_name', 'email',
                    'passport', 'birthday', 'country', 'city', 'created')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'details')

class DayAdmin(admin.ModelAdmin):
    list_display = ('date', 'location', 'event', 'max_bookings', 'total_bookings')
    change_list_template = 'admin/bookings/bookings_change_list.html'
    ordering = ['date','location','total_bookings']
    search_fields = ['date', 'location','event']
    list_filter = ['date', 'location', 'event']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['events'] = events = Event.objects.all()
        return super(DayAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('unlock/', self.unlock_days, name='unlock_days')
        ]
        return custom_urls + urls

    def unlock_days(self, request):
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        max_num = request.POST['max_num']
        selected_days = request.POST.getlist('weekdays')
        events = request.POST.getlist('events')
        
        days = Day.prepare_days(start_date, end_date, selected_days)

        for event in events:
            event = Event.objects.get(id = event)
            for day in days:
                try:
                    #####CHECK IF DAY EXISTS:
                    qs = Day.objects.filter(date = day, event = event)
                    if qs.exists():
                       pass 
                    else:
                        d = Day(date = day, max_bookings = int(max_num), 
                        total_bookings = 0, location = event.location, 
                        event = event)
                        d.save()
                except:
                    messages.error(request, "Eroare la deblocarea zilelor selectate!")
                    return HttpResponseRedirect("../")
            Event.objects.filter(id = event.id).update(last_date=end_date)

        #!!!!!!!!!!!!!!
        #DELETE OLDER DAYS
        old_days = Day.objects.filter(date__lt=date.today()-timedelta(days=1))
        for old_day in old_days:
            old_day.delete()

        messages.success(request, "Perioda {}-{} a fost deblocata cu succes".format(start_date, end_date))
        return HttpResponseRedirect("../")

admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Booking, BookingAdmin)