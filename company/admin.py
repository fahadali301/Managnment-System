from django.contrib import admin
from .models import Company,Branch,Building,Floor,Room,Asset,User,Role,Permissions


admin.site.register(Company)
admin.site.register(Permissions)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Branch)
admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Asset)
