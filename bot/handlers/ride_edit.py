from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from bot import bot
from bot.texts import START_TEXT
from bot.models import User, Ride
from .user import call_taxi


URL = "https://satellite-map.gosur.com/ru/google-earth/?ll=54.31547352165194,48.36413993118936&z=18.33342107735938&t=streets"


def edit_cost(call: CallbackQuery):
    """Изменение стоимости поездки"""
    _, user_id, ride_id = call.data.split("_")

    ride = Ride.objects.get(pk=ride_id)
    msg = bot.send_message(text="Установите вашу цену за поездку (не менее 100 руб.)")
    bot.register_next_step_handler(msg, register_cost, user_id, ride)


def register_cost(message, user_id, ride):
    """Запись цены в DB"""
    try:
        cost_ = int(message.text)
    except:
        bot.send_message(text="Цена не может быть меньше 100 руб.!", chat_id=user_id)
        call_taxi(message, status=1, pk_=ride.pk)
        return
    if cost_ < 100:
        bot.send_message(text="Цена не может быть меньше 100 руб.!", chat_id=user_id)
        call_taxi(message, status=1, pk_=ride.pk)
        return
    ride.cost = str(cost_)
    ride.save()

    call_taxi(message, status=1, pk_=ride.pk)
    return


def edit_geo_start(call: CallbackQuery):
    """Изменение адреса старта поездки"""
    _, user_id, ride_id = call.data.split("_")
    
    ride = Ride.objects.get(pk=ride_id)

    markup = ReplyKeyboardMarkup()
    btn = KeyboardButton(text="Отправить геолокацию", request_location=True)
    markup.add(btn)

    msg = bot.send_message(text="Установите адрес начала поездки\n\nМожно отправить как текстом, так и нажав на кнопку", chat_id=user_id, reply_markup=markup)
    bot.register_next_step_handler(msg, register_geo_start, user_id, ride)


def register_geo_start(message, user_id, ride):
    """Запись адреса начала поездки в DB"""
    if message.content_type == "location":
        latitude = message.location.latitude
        longitude = message.location.longitude
    else:
        ride.adress_start = message.text
        ride.save()
        call_taxi(message, status=1, pk_=ride.pk)
        return
    ride.adress_start = f"{latitude}/{longitude}"
    ride.save()
    
    call_taxi(message, status=1, pk_=ride.pk)
    return


def edit_geo_end(call: CallbackQuery):
    """Изменение адреса конца поездки"""
    _, user_id, ride_id = call.data.split("_")
    
    ride = Ride.objects.get(pk=ride_id)

    msg = bot.send_message(text="Установите адрес конца поездки\n\nМожно отправить как текстом, так и с помощью телеграмма", chat_id=user_id)
    bot.register_next_step_handler(msg, register_geo_start, user_id, ride)


def register_geo_start(message, user_id, ride):
    """Запись адреса конца поездки в DB"""
    if message.content_type == "location":
        latitude = message.location.latitude
        longitude = message.location.longitude
    else:
        ride.adress_end = message.text
        ride.save()
        call_taxi(message, status=1, pk_=ride.pk)
        return
    ride.adress_end = f"{latitude}/{longitude}"
    ride.save()
    
    call_taxi(message, status=1, pk_=ride.pk)
    return