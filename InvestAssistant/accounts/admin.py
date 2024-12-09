from django.contrib import admin
from django.contrib.admin import ModelAdmin
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
    list_display = ('pk', 'user', 'phone_number', 'balance', )
    list_editable = ('balance', 'phone_number', )
    search_fields = ('user__email', 'first_name', 'phone_number', )
    ordering = ('balance', 'user')
    list_per_page = 10

    fieldsets = [
        ('Profile Information', {
            'fields': [
                'user',
                'phone_number',
                'balance',
            ],
        }),
    ]