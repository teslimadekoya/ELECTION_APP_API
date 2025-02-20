from django.contrib import admin
from . models import User
from django.contrib.auth.models import Group

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display= ('id', 'first_name', 'last_name', 'voters_id', 'is_staff', 'role')
    search_fields = ('first_name', 'last_name', 'voters_id')


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)