import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from core.config import load_config, Config
from core.dialogs.question_dialogs import question_dialogs
from core.handlers import routers_list
from core.handlers.start_handler import update_handler
from core.middlewares.config import ConfigMiddleware
from core.services import broadcaster
from aiogram_dialog import setup_dialogs

from core.services.db_api.sqlite import create_users_tables

logger = logging.getLogger(__name__)


# DEV t.me//ElonMuskSEO
async def on_startup(bot: Bot, admin_ids: list[int]):
    create_users_tables()
    await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")


def register_global_middlewares(dp: Dispatcher, config: Config, session_pool=None):
    """
    Register global middlewares for the given dispatcher.
    Global middlewares here are the ones that are applied to all the handlers (you specify the type of update)

    :param dp: The dispatcher instance.
    :type dp: Dispatcher
    :param config: The configuration object from the loaded configuration.
    :param session_pool: Optional session pool object for the database using SQLAlchemy.
    :return: None
    """
    middleware_types = [
        ConfigMiddleware(config),
        # DatabaseMiddleware(session_pool),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


async def main():
    # Настройка уровня логирования для aiogram и asyncio на уровень DEBUG
    logging.basicConfig(format=u'%(filename)s ['
                               u'LINE:%(lineno)d] #%('
                               u'levelname)-8s [%('
                               u'asctime)s]  %('
                               u'message)s',
                        level=logging.DEBUG,
                        # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                        )
    logging.getLogger('aiogram').setLevel(logging.DEBUG)
    logging.getLogger('asyncio').setLevel(logging.DEBUG)
    logging.getLogger('dispatcher.py').setLevel(logging.DEBUG)

    config = load_config(".env")
    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    dp.include_routers(*routers_list, question_dialogs)
    dp.chat_join_request.register(update_handler, F.chat.id == "-1002017349679")
    # register_global_middlewares(dp, config)

    setup_dialogs(dp)

    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот був вимкнений!")
