from typing import Any

from django.views.generic import TemplateView

from punq import Container

from core.apps.chats.entities.messages import MessageStat
from core.apps.chats.services.messages import BaseMessageService
from core.apps.common.mixins import (
    AdminMixin,
    DataMixin,
)
from core.project.containers import get_container


class GroupMessageStatsView(AdminMixin, DataMixin, TemplateView):
    template_name = 'chats/group_message_stat.html'
    title_page = 'Статистика | Групповые чаты'

    def test_func(self) -> bool | None:
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        container: Container = get_container()
        message_service: BaseMessageService = container.resolve(BaseMessageService)

        message_stats: list[MessageStat] = message_service.get_message_stat()
        return self.get_mixin_context(
            context=context,
            stats=message_stats,
        )
