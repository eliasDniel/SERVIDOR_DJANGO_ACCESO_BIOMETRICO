from django.contrib import admin

from .models import RegistroEntrada,Device

# Register your models here.
admin.site.register(RegistroEntrada)
admin.site.register(Device)
