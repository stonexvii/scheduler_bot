from .commands import command_router
from .callback_handlers import callback_router

handlers = [
    command_router,
    callback_router,
]
