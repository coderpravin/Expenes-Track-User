from django.contrib import admin
from .models import Category, Expenses


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)

class ExepensesAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'amount', 'date')
    search_fields = ('title', 'category__name')
    list_filter = ('date', 'category')
admin.site.register(Category, CategoryAdmin)
admin.site.register(Expenses, ExepensesAdmin)   