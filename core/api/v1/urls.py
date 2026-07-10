from ninja import Router

from core.api.v1.chats.handlers import router as chat_router
from core.api.v1.messages.handlers import router as message_router
from core.api.v1.users.handlers import router as user_router


router = Router()

router.add_router(prefix='users/', router=user_router)
router.add_router(prefix='chats/', router=chat_router)
router.add_router(prefix='chats/', router=message_router)
