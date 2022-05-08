from django.db import models
from django.core.validators import FileExtensionValidator
from datetime import timedelta, date, datetime

class Location(models.Model):
    name = models.CharField("Denumire locatie",max_length=100)
    details = models.CharField("Detalii locatie",max_length=100)
    class Meta:
        verbose_name = 'Locatie'
        verbose_name_plural = 'Locatii'

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField("Articol",max_length=200)
    details = models.CharField("Detalii",max_length=200, blank = True, null = True)
    location = models.ForeignKey(Location, verbose_name = 'Locatie',on_delete = models.CASCADE)
    address = models.CharField("Adresa", max_length=200)
    is_lawyer = models.BooleanField("Este pentru avocati",default = False)
    last_date = models.DateField("Ultima zi deblocata", blank = True, null = True)
    class Meta:
        verbose_name = 'Articol'
        verbose_name_plural = 'Articole'

    def __str__(self):
        return self.name


class Day(models.Model):
    date = models.DateField("Data", auto_now=False, auto_now_add=False)
    max_bookings = models.IntegerField("Numar maxim de programari pe zi")
    total_bookings = models.IntegerField("Total programari", blank = True, null = True)
    location = models.ForeignKey(Location, verbose_name = 'Locatie', on_delete = models.CASCADE)
    event = models.ForeignKey(Event, verbose_name = 'Articol', on_delete = models.CASCADE)
    class Meta:
        verbose_name = 'Zi deblocata'
        verbose_name_plural = 'Zile deblocate'

    def prepare_days(start, end, selected_days):
        def daterange(date1, date2):
            for n in range(int ((date2 - date1).days)+1):
                yield date1 + timedelta(n)

        weekdays = [0,1,2,3,4,5,6]

        #transform from "2019-01-01" to date(2019, 01, 01)
        start = datetime.strptime(start,"%Y-%m-%d")
        end = datetime.strptime(end,"%Y-%m-%d")

        #convert selected_days list from strings to integers
        for i in range(0, len(selected_days)): 
            selected_days[i] = int(selected_days[i]) 

        #a temporary list to store weekdays
        temp_list = []
        for item in weekdays:
            if item not in selected_days:
                temp_list.append(item)
        #final days list
        days_list = []

        for dt in daterange(start, end):
            if dt.weekday() not in temp_list:       
                days_list.append(dt.strftime("%Y-%m-%d"))
        return days_list       

    def __str__(self):
        return str(self.date)

class Booking(models.Model):
    email = models.EmailField("Adresa de E-mail",max_length=254)
    event = models.ForeignKey(Event, verbose_name = 'Articol', on_delete= models.CASCADE)
    created = models.DateTimeField("Creat la data de",auto_now_add=True)
    past = models.BooleanField("Data depasita",default = False)
    location = models.ForeignKey(Location, verbose_name = 'Locatie', on_delete = models.CASCADE)
    date = models.DateField("Data programare",auto_now=False, auto_now_add=False)
    #day = models.ForeignKey(Day, on_delete = models.CASCADE)
    first_name = models.CharField("Nume",max_length = 100)
    last_name = models.CharField("Prenume",max_length = 100)
    birthday = models.DateField("Data nasterii",auto_now=False, auto_now_add=False)
    country = models.CharField("Tara",max_length=100)
    city = models.CharField("Oras",max_length=100)
    passport = models.CharField("Nume pasaport",max_length=100)
    is_lawyer = models.BooleanField("Este avocat",default = False)

    empower = models.FileField("Imputernicire avocatiala",
    upload_to='uploads/%Y/%m/%d/', null = True, blank = True, 
    validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'png', 'jpeg'])])

    lawyer_id = models.FileField("Legitimatie avocat",
    upload_to = 'uploads/%Y/%m/%d/', null = True, blank = True, 
    validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'png', 'jpeg'])])

    class Meta:
        verbose_name = 'Programare'
        verbose_name_plural = 'Programari'

    def __str__(self):
        return self.first_name + " " + self.event