from django.contrib import admin
from .models import Task


class TasksAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
# Register your models here.
admin.site.register(Task, TasksAdmin) #Se registra el modelo en el panel de administración