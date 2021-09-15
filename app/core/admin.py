from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ModelForm
from core import models


class UserCreationForm(ModelForm):
    '''Overriding User creation form for Django Admin Panel, so it saves
    the password as a hash'''

    class Meta:
        model = models.User
        fields = '__all__'

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    '''Overrides the Django Admin Interface for User Model'''
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal Info'), {'fields': ('name',)}),
        (
            ('Permissions'),
            {'fields': ('is_staff', 'is_superuser', 'account_plan')}
        ),
        (('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.AccountPlan)
admin.site.register(models.BaseImage)
admin.site.register(models.Thumbnail)
admin.site.register(models.Link)

# Create superuser for admin use in case it doesn't exist
