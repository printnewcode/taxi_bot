from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import bot
from bot.texts import START_TEXT
from bot.models import User, Ride


def menu(user):
    """Меню для пользователя"""
    MENU_BUTTONS = InlineKeyboardMarkup()
    menu_call = InlineKeyboardButton(text="Вызвать такси", callback_data=f"taxi_{user.telegram_id}")
    MENU_BUTTONS.add(menu_call)

    bot.send_message(
        user.telegram_id,
        f"👋 Привет, {user.name}!\n\n"
        f"💼 Ваша роль: Пользователь\n"
        f"⭐ Рейтинг: {user.rating}",
        reply_markup=MENU_BUTTONS,
    )


def call_taxi(call: CallbackQuery):
    """Вызов такси"""
    ride = Ride.objects.create(
        user=User.objects.get(telegram_id=call.message.chat.id),
    )  # Создание экземляра модели поездки

    TAXI_KEYBOARDS = InlineKeyboardMarkup()
    taxi_price = InlineKeyboardButton(text="💸 Установить стоимость поездки",
                                      callback_data=f"cost_{call.message.chat.id}_{ride.pk}")
    taxi_geo_start = InlineKeyboardButton(text="📍 Установить адрес откуда",
                                          callback_data=f"start-adress_{call.message.chat.id}_{ride.pk}")
    taxi_geo_end = InlineKeyboardButton(text="📍 Установить адрес куда",
                                        callback_data=f"end-adress_{call.message.chat.id}_{ride.pk}")
    TAXI_KEYBOARDS.add(taxi_price).add(taxi_geo_start).add(taxi_geo_end)

    bot.send_message(
        call.message.chat.id,
        text="👋 Привет! Для вызова такси укажите условия поездки: Стоимость, Точки начала и конца маршрута",
        reply_markup=TAXI_KEYBOARDS
    )
