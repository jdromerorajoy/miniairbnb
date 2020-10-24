from django.contrib import admin
from .models import User,Estate,RentDate,City,Service
from django.contrib.admin.models import LogEntry

#admin.site.register(Owner)
#admin.site.register(User)
admin.site.register(City)
admin.site.register(Service)

class EstateAdmin(admin.ModelAdmin):
        list_display= ('title','owner','dailyRate','pax','city')
        search_fields = ('title', 'owner__username')
admin.site.register(Estate,EstateAdmin)

class RentDateAdmin(admin.ModelAdmin):
        fields = ['estate', 'dateFrom', 'dateTo']
        list_display = ('dateFrom', 'estate', 'dateTo')
        search_fields = ('dateFrom','estate__title','dateTo')
admin.site.register(RentDate,RentDateAdmin)

LogEntry.objects.all().delete()