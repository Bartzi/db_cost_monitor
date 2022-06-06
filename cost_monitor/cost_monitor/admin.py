from django.contrib import admin

from cost_monitor.models import Journey, Connection, Fare

admin.site.register(Journey)
admin.site.register(Connection)
admin.site.register(Fare)