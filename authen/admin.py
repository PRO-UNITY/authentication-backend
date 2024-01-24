from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authen.models import CustomUser, Country, Gender


class NewMyUser(UserAdmin):
    model = CustomUser
    list_display = ["username", "first_name", "last_name", "id"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("country", "phone", "gender",),}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("country", "phone", "gender",),}),)


admin.site.register(CustomUser, NewMyUser)

admin.site.register(Country)
admin.site.register(Gender)