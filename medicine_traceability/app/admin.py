from django.contrib import admin
from app.models import firm_info,medicine
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class firm_profile_Inline(admin.StackedInline):
    model = firm_info
    can_delete = False
    verbose_name_plural = 'firm_profile'

class CustomizedUserAdmin(UserAdmin):
    inlines = (firm_profile_Inline, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
admin.site.register(firm_info)
admin.site.register(medicine)