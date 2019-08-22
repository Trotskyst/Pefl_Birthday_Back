from django.contrib import admin
from managers.models import *

class ChempsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link')


class DivsAdmin(admin.ModelAdmin):
    list_display = ('id', 'chemp', 'name', 'link', 'sort')


class TeamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'div', 'name', 'link')


class ManagerLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'link')


class ManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'manager', 'gender', 'timestamp', 'birthday', 'link_photo', 'team')


admin.site.register(Gender)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Chemps, ChempsAdmin)
admin.site.register(Divs, DivsAdmin)
admin.site.register(Teams, TeamsAdmin)
admin.site.register(ManagerLink, ManagerLinkAdmin)
