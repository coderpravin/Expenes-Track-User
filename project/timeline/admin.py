from django.contrib import admin
from .models import Months, Year, ContactMessage

admin.site.register(Months)

@admin.register(Year)
class YearAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return Year.objects.count() < 2


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'message', 'created_at')
    search_fields = ('name', 'email')

    #Disable add button
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request):
        return False
    