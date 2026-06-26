from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'position', 'employment_type', 'status', 'joining_date')
    list_filter = ('status', 'employment_type')
    search_fields = ('user__username', 'user__email', 'position')

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Name'
