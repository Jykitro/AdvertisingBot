from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def admin_menu():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📮 Рассылка", callback_data="user_mailing"))
    builder.row(InlineKeyboardButton(text="📮 Рассылка Pro", callback_data="user_mailing_pro"))
    # builder.row(InlineKeyboardButton(text="📊 Полная статистика", callback_data="full_statistics"))
    builder.row(InlineKeyboardButton(text="📡 Выгрузка базы пользывателей", callback_data="upload_database"))
    return builder.as_markup()


def start_menu():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📝 Оформить заявку", callback_data="get_paid"))
    return builder.as_markup()


def mailing_btn(text_btn, btn_url):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text_btn, url=btn_url))
    return builder.as_markup()
