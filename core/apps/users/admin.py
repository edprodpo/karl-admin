from django.contrib import admin

from core.apps.chats.admin import MessageInline
from core.apps.users.models.users import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('vk_id', 'name', 'email', 'created_at')
    list_display_links = ('vk_id', 'email')
    readonly_fields = ('vk_id', 'name', 'created_at', 'updated_at')
    search_fields = ('vk_id', 'name', 'email')

    inlines = (MessageInline,)
