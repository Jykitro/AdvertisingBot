"""Import all routers and add them to routers_list."""
# from .main_handler import main_handler
from .start_handler import StartHandler
from .admin_handlers import AdminHandler

# DEV t.me//ElonMuskSEO
routers_list = [
    StartHandler,
    AdminHandler,

]

__all__ = [
    "routers_list",
]
