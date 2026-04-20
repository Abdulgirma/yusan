from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'reg_number', 'department', 'phone_number', 'created_at']
    search_fields = ['full_name', 'reg_number', 'phone_number']
    list_filter = ['department']
