from django.contrib import admin

from .models import Task,Cliente,Membresia
class TasksAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
# Register your models here.
admin.site.register(Task,TasksAdmin)
admin.site.register(Cliente)
admin.site.register(Membresia)
