from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from core.apps.chats.models.chats import Chat as ChatModel
from core.apps.chats.models.messages import Message as MessageModel


class MessageInline(admin.TabularInline):
    model = MessageModel
    readonly_fields = ('id', 'user', 'chat', 'request', 'response', 'created_at', 'updated_at')
    extra = 0
    ordering = ('-created_at',)


@admin.register(ChatModel)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'title', 'type_chat', 'is_active', 'created_at')
    list_display_links = ('chat_id', 'title')
    readonly_fields = ('chat_id', 'title', 'type_chat', 'created_at', 'updated_at')
    search_fields = ('chat_id', 'title')
    actions = ('allow_chat', 'revoke_access')

    inlines = (MessageInline,)

    @admin.action(description='Разрешить доступ')
    def allow_chat(self, request: HttpRequest, queryset: QuerySet[ChatModel]) -> None:
        count = queryset.update(is_active=True)
        self.message_user(request, f'Разрешён доступ для {count} чатов')

    @admin.action(description='Забрать доступ')
    def revoke_access(self, request: HttpRequest, queryset: QuerySet[ChatModel]) -> None:
        count = queryset.update(is_active=False)
        self.message_user(request, f'Доступ закрыт для {count} чатов')


@admin.register(MessageModel)
class MessageModel(admin.ModelAdmin):
    list_display = ('id', 'user', 'chat', 'request', 'response', 'created_at')
    list_display_links = ('id', 'user', 'chat')
    list_select_related = ('user', 'chat')

    readonly_fields = ('id', 'user', 'chat', 'request', 'response', 'created_at', 'updated_at')
