from time import sleep
from aiogram import Router, Bot
from aiogram.types import Message, ChatJoinRequest, CallbackQuery
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode
from core.state.state import QuestionState
from core.msg import msg_start
from core.keyboards.inline import start_menu
from core.services.db_api.sqlite import register_user, check_filled_out
StartHandler = Router()


@StartHandler.message(CommandStart())
async def start_handler(message: Message):
    register_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                  message.from_user.last_name)
    if not check_filled_out(message.from_user.id):
        msg = msg_start.format(userFirstName=message.from_user.first_name)
        await message.answer(text=msg, reply_markup=start_menu())
    else:
        await message.answer(text="☎️ Вы уже подали заявку ожидайте звонка")


@StartHandler.callback_query(lambda query: query.data == 'get_paid')
async def get_paid_handler(call:CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(QuestionState.age, mode=StartMode.RESET_STACK)


@StartHandler.chat_join_request()
async def update_handler(chat_member: ChatJoinRequest, bot: Bot):
    await bot.send_message(chat_id=chat_member.from_user.id, text="Спасибо за заявку !!")
    sleep(30)
    await chat_member.approve()
