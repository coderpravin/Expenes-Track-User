from django.contrib import admin
from .models import Months, Year

admin.site.register(Months)

@admin.register(Year)
class YearAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return Year.objects.count() < 2
