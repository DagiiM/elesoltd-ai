from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserChangeForm

# Register your models here.
class AccountAdmin(BaseUserAdmin):
    form = UserChangeForm

    list_display = ('email','first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('date_joined',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    def get_readonly_fields(self, request, obj=None):
        # Allow users to change their own password
        if obj is not None and obj == request.user:
            return ('username','email','phone_number','password')
        return super().get_readonly_fields(request, obj)
    
admin.site.register(User,AccountAdmin)