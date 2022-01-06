from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, Follow


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = []
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_admin',
        'is_superuser',
    )
    model = CustomUser
    list_filter = ('first_name', 'email',)

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',)})
    )

    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Permissions', {'fields': ('is_active',)})
    )

    search_fields = ('username', 'email', 'first_name', 'last_name',)
    ordering = ('email',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    list_filter = ('user',)
