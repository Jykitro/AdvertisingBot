import operator

from aiogram import Bot
from aiogram_dialog import (
    Dialog, Window, LaunchMode, DialogManager,
)
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import ManagedRadio, Next, Radio, Column, RequestContact, Button, Cancel

from core.services.db_api.sqlite import update_user
from core.state.state import QuestionState
from aiogram.types import Message


# DEV t.me//ElonMuskSEO
async def que_date(**kwargs):
    age_list = [
        ("Меньше 18 лет", '1'),
        ("18 - 25 лет", '2'),
        ("26 - 35 лет", '3'),
        ("36 - 45 лет", '4'),
        ("45+ лет", '5'),
    ]
    about_us = [
        ("От друзей и знакомых", '1'),
        ("Реклама в интернете", '2'),
        ("Реклама на телевидении", '3')
    ]
    financial_goal = [
        ("Да, я имею финансовую цель.", "1"),
        ("Нет, у меня нет финансовых целей.", "2"),
        ("Я не думал об этом.", "3"),

    ]
    take_time = [
        ("Не более часа в день", "1"),
        ("Несколько часов в день", "2"),
        ("Один раз в неделю", "3"),
        ("Один раз в месяц", "4"),

    ]
    partnership_participation = [
        ("Да", "1"),
        ("Нет", "2"),
        ("Хочу узнать больше", "3"),
    ]
    your_nationality = [
        ("Гражданство России", "1"),
        ("Гражданство Казахстан", "2"),
        ("Гражданство другой страны", "3"),
    ]

    return {
        "age_list": age_list,
        'count': len(age_list),

        'About_us': about_us,
        "count_about": len(about_us),

        "Financial_goal": financial_goal,
        "count_financial_goal": len(financial_goal),

        "take_time": take_time,
        "count_take": len(take_time),

        "partnership_participation": partnership_participation,
        "count_participation": len(partnership_participation),

        "your_nationality": your_nationality,
        "count_nationality": len(your_nationality),
    }


async def name_handler(
        message: Message,
        widget: MessageInput,
        manager: DialogManager,
):
    manager.dialog_data["name"] = message.text
    await manager.next()


async def phone_handler(
        message: Message,
        widget: MessageInput,
        manager: DialogManager,
):
    manager.dialog_data["phone_number"] = message.contact.phone_number
    await manager.next()


async def get_user_data(dialog_manager: DialogManager, bot: Bot, **kwargs):
    radio_que1: ManagedRadio = dialog_manager.find("age")
    radio_que2: ManagedRadio = dialog_manager.find("about_us")
    radio_que3: ManagedRadio = dialog_manager.find("financial_goal")
    radio_que4: ManagedRadio = dialog_manager.find("take_time")
    radio_que5: ManagedRadio = dialog_manager.find("participation")
    radio_que6: ManagedRadio = dialog_manager.find("nationality")
    update_user(dialog_manager.event.from_user.id, radio_que1.get_checked(), radio_que2.get_checked(),
                radio_que3.get_checked(), radio_que4.get_checked(), radio_que5.get_checked(), radio_que6.get_checked(),
                dialog_manager.dialog_data.get("name"), dialog_manager.dialog_data.get("phone_number"), )
    await bot.send_message(chat_id="-1002145855934", text="Lead Info\n\n"
                                                          f"Name: {dialog_manager.dialog_data.get('name')}\n"
                                                          f"Phone Number: {dialog_manager.dialog_data.get('phone_number')}\n"
                                                          f"TG Username: @{dialog_manager.event.from_user.username}\n"
                                                          f"Que 1: {radio_que1.get_checked()}\n"
                                                          f"Que 2: {radio_que2.get_checked()}\n"
                                                          f"Que 3: {radio_que3.get_checked()}\n"
                                                          f"Que 4: {radio_que4.get_checked()}\n"
                                                          f"Que 5: {radio_que5.get_checked()}\n"
                                                          f"Que 6: {radio_que6.get_checked()}\n"
                           )
    return {
        "name": dialog_manager.dialog_data.get("name"),
    }


async def handler(dialog_manager: DialogManager, message: Message):
    # my actions
    await message.answer("sps")
    await dialog_manager.done()


question_dialogs = Dialog(
    #   1
    Window(
        Const(
            "Сколько вам лет?",
        ),
        Column(
            Radio(
                Format("🔘 {item[0]}"),  # E.g `🔘 Apple`
                Format("⚪️ {item[0]}"),
                id="age",
                item_id_getter=operator.itemgetter(1),
                items="age_list",
                on_click=Next()
            )
        ),
        state=QuestionState.age,
        getter=que_date,

    ),

    # 2
    Window(
        Const("Откуда вы узнали о проекте"),
        Column(
            Radio(
                Format("🔘 {item[0]}"),
                Format("⚪️ {item[0]}"),
                id="about_us",
                item_id_getter=operator.itemgetter(1),
                items="About_us",
                on_click=Next()
            ),
        ),
        state=QuestionState.how_did_you_hear_about_us,
        getter=que_date,
    ),
    # 3
    Window(
        Const(
            "Каковы ваши финансовые цели, и хотели бы вы их достичь в ближайшем будущем?",
        ),
        Column(
            Radio(
                Format("🔘 {item[0]}"),  # E.g `🔘 Apple`
                Format("⚪️ {item[0]}"),
                id="financial_goal",
                item_id_getter=operator.itemgetter(1),
                items="Financial_goal",
                on_click=Next()
            )
        ),
        state=QuestionState.financial_goal,
        getter=que_date,

    ),
    # 4
    Window(
        Const(
            "Сколько времени Вы готовы уделять заработку в своем смартфоне?",
        ),
        Column(
            Radio(
                Format("🔘 {item[0]}"),
                Format("⚪️ {item[0]}"),
                id="take_time",
                item_id_getter=operator.itemgetter(1),
                items="take_time",
                on_click=Next()
            )
        ),
        state=QuestionState.take_time,
        getter=que_date,

    ),
    Window(
        Const(
            "Знаете ли Вы, что партнерское участие в программе <b>«НОРНИКЕЛЬ»</b> позволит вам стать финансово грамотным "
            "человеком и создать стабильный пассивный доход?"),
        Column(
            Radio(
                Format("🔘 {item[0]}"),
                Format("⚪️ {item[0]}"),
                id="participation",
                item_id_getter=operator.itemgetter(1),
                items="partnership_participation",
                on_click=Next()
            ),
        ),

        state=QuestionState.partnership_participation,
        getter=que_date,
    ),
    Window(
        Const("Какое у вас гражданство?"),
        Column(
            Radio(
                Format("🔘 {item[0]}"),
                Format("⚪️ {item[0]}"),
                id="nationality",
                item_id_getter=operator.itemgetter(1),
                items="your_nationality",
                on_click=Next()
            ),
        ),
        state=QuestionState.your_nationality,
        getter=que_date,
    ),
    # Input Name
    Window(
        Const(
            "Поздравляем, вам стали доступны инвестиции на платформе <b>«НОРНИКЕЛЬ»</b>! Чтобы начать зарабатывать, "
            "оставьте свои контактные данные. Менеджер свяжется с Вами в порядке очереди:\n"),
        Const("Введите ваше ФИО"),
        MessageInput(name_handler),
        state=QuestionState.name,
        preview_add_transitions=[Next()]
    ),
    # Input phone
    Window(
        Const("Отправьте свой контакт"),
        RequestContact(Const("👤 Отправить контакт")),
        MessageInput(phone_handler),
        markup_factory=ReplyKeyboardFactory(
            input_field_placeholder=Format("{event.from_user.username}"),
            resize_keyboard=True,
        ),
        state=QuestionState.phone_number,
        preview_add_transitions=[Next()]
    ),
    Window(
        Format("<b>Поздравляем</b> {name}, Вам открыт доступ к инвестиционной платформе <b>«Норникель Инвестиции»</b>"
              "Специалист свяжется с Вами в порядке очереди.\n"),
        Button(
            text=Const("Хорошо"),
            id="confirm", on_click=Cancel()),
        state=QuestionState.confirm,
        getter=get_user_data,
        preview_add_transitions=[Cancel()]
    ),

)
