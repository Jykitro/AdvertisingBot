from aiogram.filters import BaseFilter
from aiogram.types import Message

from core.config import Config, load_config

config = load_config(".env")


# DEV t.me//ElonMuskSEO
class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message) -> bool:
        return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin
