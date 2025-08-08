# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'profile_picture')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    
    # The forms to add and change user instances
    # These are required because we are customizing UserAdmin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'profile_picture'),
        }),
    )
    
    # Fields to display in the user list
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_verified', 'profile_picture')
    
    # Fields to search by
    search_fields = ('email', 'first_name', 'last_name')
    
    # How the list is ordered. THIS IS THE DIRECT FIX FOR THE ERROR.
    ordering = ('email',)

    # We must override fieldsets to remove 'username'
    # and use 'email' instead.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


# Register your User model with your custom admin class
admin.site.register(User, CustomUserAdmin)