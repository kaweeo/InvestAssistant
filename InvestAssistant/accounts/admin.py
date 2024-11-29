from django.contrib import admin
from unfold.admin import ModelAdmin

from InvestAssistant.accounts.models import Profile, AppUser

admin.site.site_header = "InvestAssistant Admin"
admin.site.site_title = "InvestAssistant Admin Portal"
admin.site.index_title = "Welcome to the InvestAssistant Administration"

@admin.register(AppUser)
class AppUserAdmin(ModelAdmin):
    list_display = ('email', 'date_joined', 'last_login', )
    list_filter = ('is_staff', 'is_active')


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    model = Profile

    list_filter = ('balance', )
    list_display = ('pk', 'user_id', 'user', 'phone_number', 'balance', )
    search_fields = ('user__email', 'first_name', 'phone_number', )
    ordering = ('balance', 'user_id')
    list_per_page = 10

    fieldsets = (
            (None, {'fields': ('user', 'password')}),
            ('Personal info', {'fields': ()}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
            ('Important dates', {'fields': ('last_login',)})
)