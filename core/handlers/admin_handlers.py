from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command, StateFilter

from core.filters.AdminFilter import AdminFilter
from aiogram.types import FSInputFile
from core.services import broadcaster
from core.keyboards.inline import admin_menu, mailing_btn
from aiogram import Bot
from core.services.db_api.sqlite import all_user_id, get_amount_users, get_today_user, upload_dump
from datetime import datetime

AdminHandler = Router()
AdminHandler.message.filter(AdminFilter())


class AdminState(StatesGroup):
    mailing_text = State()
    mailing_text_pro = State()
    mailing_btn_text = State()
    mailing_url_pro = State()


# DEV t.me//ElonMuskSEO

@AdminHandler.message(F.text, Command("admin"))
async def start_handler(message: Message):
    with open("core/handlers/admin.jpg", "rb") as img:
        await message.answer_photo(photo=BufferedInputFile(img.read(), filename="admin.jpg"),
                                   caption="<b>Добро пожаловать в ADMIN PANEL</b>\n\n"
                                           "<b>Версия бота</b>: 1.1 \n\n"
                                           f"<b>Твой ID</b>: {message.from_user.id}\n\n"
                                           f"<b>Всего пользователей в боте</b>: {get_amount_users()}\n"
                                           f"<b>Всего пользователей за сегодня</b>: {get_today_user()}\n",
                                   reply_markup=admin_menu())


@AdminHandler.callback_query(lambda call: call.data == "upload_database")
async def mailing_handler(call: CallbackQuery):
    upload_dump()
    today = datetime.now().date()
    await call.message.answer_document(document=FSInputFile(path=f'dump/{today}.xlsx'),
                                       caption="⚠️ <b>Dump SQL Database</b>")


@AdminHandler.callback_query(lambda call: call.data == "user_mailing")
async def mailing_handler(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите текст для начала рассылки:\n'
                              'Также поддерживаю фото с  описанием.')
    await state.set_state(AdminState.mailing_text)


# Mailing Pro
@AdminHandler.callback_query(lambda call: call.data == "user_mailing_pro")
async def mailing_pro_handler(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text="💎 Режим рассылки <b>RPO</b>\n\n"
                                   "1. Введите текст или фото с текстом:")
    await state.set_state(AdminState.mailing_text_pro)


@AdminHandler.message(StateFilter(AdminState.mailing_text_pro))
async def mailing_pro_text_handler(message: Message, state: FSMContext):
    if message.content_type == "photo":
        await state.update_data(mailingpro_text=message.caption)
        await state.update_data(photo_allowed=True, photo_id=message.photo[0].file_id)
    if message.content_type == "text":
        await state.update_data(mailingpro_text=message.text)
    await message.answer(text="2. Введите текст для Inline Кнопки")
    await state.set_state(AdminState.mailing_btn_text)


@AdminHandler.message(StateFilter(AdminState.mailing_btn_text))
async def mailing_text_handler(message: Message, state: FSMContext):
    await state.update_data(mailing_btn_text=message.text)
    await message.answer(text="3. Введите URL для Inline кнопки")
    await state.set_state(AdminState.mailing_url_pro)


# Pro-mode
@AdminHandler.message(StateFilter(AdminState.mailing_url_pro))
async def mailing_url_handler(message: Message, bot: Bot, state: FSMContext):
    users_list = [item[0] for item in all_user_id()]
    data = await state.get_data()

    if data.get('photo_allowed'):
        await broadcaster.broadcast(bot, users=users_list, photo=data.get('photo_id'), text=data.get("mailingpro_text"),
                                    reply_markup=mailing_btn(data.get('mailing_btn_text'), message.text))
    else:
        await broadcaster.broadcast(bot, users=users_list, text=data.get("mailingpro_text"),
                                    reply_markup=mailing_btn(data.get('mailing_btn_text'), message.text))
    await message.answer(text="✅ Рассылка выполнена успешно.")


@AdminHandler.message(StateFilter(AdminState.mailing_text))
async def mailing_text_handler(message: Message, bot: Bot):
    users_list = [item[0] for item in all_user_id()]
    if message.content_type == "photo":
        await broadcaster.broadcast(bot, users=users_list, photo=message.photo[0].file_id, text=message.caption)
    elif message.content_type == "text":
        await broadcaster.broadcast(bot, users=users_list, text=message.text)
    await message.answer(text="✅ Рассылка выполнена успешно.")


