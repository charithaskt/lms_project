from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, Profile

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin','fullname')
    list_filter = ('admin','fullname')
    fieldsets = (
        (None, {'fields': ('email', 'password','fullname')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin','staff','active','groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','fullname')}
        ),
    )
    search_fields = ('email','fullname')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Permission)

# Remove Group Model from admin. We're not using it.
#admin.site.unregister(Group)
