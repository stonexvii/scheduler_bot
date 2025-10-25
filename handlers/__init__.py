from .callback_handlers import callback_router
from .commands import command_router

handlers = [
    command_router,
    callback_router,
]
