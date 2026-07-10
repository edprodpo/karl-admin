from django.urls import path

from core.apps.chats.views import GroupMessageStatsView


app_name = 'chats'


urlpatterns = [
    path(
        route='messages/stats/group/',
        view=GroupMessageStatsView.as_view(),
        name='group_stats',
    ),
]
