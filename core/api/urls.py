from django.urls import path
from ninja import NinjaAPI

from core.api.v1.urls import router as v1_router


api = NinjaAPI(
    title='Family nutrition bot',
)

api.add_router(prefix='v1/', router=v1_router)


urlpatterns = [
    path('', api.urls),
]
