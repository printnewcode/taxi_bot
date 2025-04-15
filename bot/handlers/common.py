from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, \
    ReplyKeyboardMarkup

from bot import bot
from bot.texts import START_TEXT
from .user import menu
from .driver import menu_driver
from bot.models import User


def start(message: Message):
    """
    Cтартовое сообщение. Выбор пользователем своей роли (Водитель или Пользователь), если не зарегистрирован.
    Получение меню, если зарегестрирован
    """
    user = User.objects.filter(telegram_id=message.chat.id)
    if not user.exists or (not user.is_driver and not user.is_user):
        START_BUTTONS = InlineKeyboardMarkup()
        start_user = InlineKeyboardButton(text="Я пользователь 👤", callback_data=f"start_user_{message.chat.id}")
        start_driver = InlineKeyboardButton(text="Я водитель 🚕", callback_data=f"start_driver_{message.chat.id}")
        START_BUTTONS.add(start_user).add(start_driver)

        bot.send_message(text=START_TEXT, reply_markup=START_BUTTONS, chat_id=message.chat.id)
        user = User.objects.create(
            telegram_id=message.chat.id,
            name=message.from_user.first_name + message.from_user.last_name if message.from_user.last_name is not None else message.from_user.first_name,
            username=message.from_user.username
        )
        user.save()
    else:
        user = user.first()
        if user.is_user:
            menu(user)
        if user.is_driver:
            menu_driver(user)


def register_role(call: CallbackQuery):
    """Запись роли пользователя в DB"""
    _, role, id_ = call.data.split("_")
    user = User.objects.get(telegram_id=id_)
    if role == "user":
        user.is_user = True
        user.is_driver = False
    else:
        user.is_user = False
        user.is_driver = True
    user.save()
    get_number(id_=call.message.chat.id)


def get_number(id_):
    MARKUP = ReplyKeyboardMarkup()
    btn = KeyboardButton("Предоставить номер телефона", request_contact=True)
    MARKUP.add(btn)
    msg = bot.send_message(
        text="Для продолжения необходимо предоставить номер телефона",
        chat_id=id_,
        reply_markup=MARKUP,
    )
    bot.register_next_step_handler(msg, register_number)


def register_number(message):
    contact_number = message.contact.phone_number

    user = User.objects.get(telegram_id=message.chat.id)
    user.number = contact_number
    user.save()

    bot.send_message(text="Мы получили ваш номер! Теперь вы можете пользоваться нашим ботом", chat_id=message.chat.id)

    if user.is_user:
        menu(user)
    if user.is_driver:
        menu_driver(user)
