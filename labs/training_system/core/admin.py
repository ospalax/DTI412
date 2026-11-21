# Register your models here.

from django.contrib import admin
from .models import Department, Employee, Course, TrainingRecord

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_code', 'first_name', 'last_name', 'department', 'salary',
                    'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('employee_code', 'first_name', 'last_name', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'capacity')
    search_fields = ('code', 'title')

@admin.register(TrainingRecord)
class TrainingRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'course', 'enrollment_date', 'completion_status', 'score')
    list_filter = ('completion_status', 'enrollment_date')
    search_fields = ('employee__employee_code', 'employee__last_name', 'course__code')

