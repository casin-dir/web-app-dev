from django.contrib import admin
from django.contrib import admin
from .models import Team

# Register your models here.
class TeamAdmin(admin.ModelAdmin):
    pass
admin.site.register(Team, TeamAdmin)