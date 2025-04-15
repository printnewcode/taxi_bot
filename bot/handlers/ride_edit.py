from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import bot
from bot.texts import START_TEXT
from bot.models import User, Ride


def edit_cost(call: CallbackQuery):
    """Изменение стоимости поездки"""
    _, user_id, ride_id = call.data.split("_")

    msg = bot.send_message(text="Установите вашу цену за поездку (не менее 100 руб.)")
    bot.register_next_step_handler(msg, register_cost)


def register_cost(message):
    ...
