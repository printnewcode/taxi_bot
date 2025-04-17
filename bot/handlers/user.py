from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import bot
from bot.texts import START_TEXT
from bot.keyboards import PAY_TYPE_KEYBOARD
from bot.models import User, Ride


def menu(user):
    """Меню для пользователя"""
    """MENU_BUTTONS = InlineKeyboardMarkup()
    menu_call = InlineKeyboardButton(text="Вызвать такси", callback_data=f"taxi_{user.telegram_id}")
    MENU_BUTTONS.add(menu_call)"""

    bot.send_message(
        user.telegram_id,
        f"👋 Привет, {user.name}!\n\n"
        f"💼 Ваша роль: Пользователь\n"
        f"⭐ Рейтинг: {user.rating}",
    )


def call_taxi(message: Message, status=0, pk_=0):
    """Вызов такси"""
    if status == 0:
        ride = Ride.objects.create(
            user=User.objects.get(telegram_id=message.chat.id),
        )  # Создание экземляра модели поездки
    else:
        ride = Ride.objects.get(pk=pk_)

    taxi_keyboards = InlineKeyboardMarkup()
    taxi_price = InlineKeyboardButton(text=f"💸 Установить стоимость поездки: {ride.cost} руб.",
                                      callback_data=f"cost_{message.chat.id}_{ride.pk}")
    taxi_geo_start = InlineKeyboardButton(text=f"📍 Установить адрес откуда: {ride.adress_start}",
                                          callback_data=f"start-adress_{message.chat.id}_{ride.pk}")
    taxi_geo_end = InlineKeyboardButton(text=f"📍 Установить адрес куда: {ride.adress_end}",
                                        callback_data=f"end-adress_{message.chat.id}_{ride.pk}")
    taxi_pay_type = InlineKeyboardButton(text=f"📍 Установить тип оплаты: {ride.pay_type}",
                                         callback_data=f"pay-type_{message.chat.id}_{ride.pk}")
    taxi_call_ = InlineKeyboardButton(text="Вызвать такси!",
                                      callback_data=f"taxi-call_{ride.pk}")
    taxi_keyboards.add(taxi_price).add(taxi_geo_start).add(taxi_geo_end).add(taxi_pay_type).add(taxi_call_)

    bot.send_message(
        message.chat.id,
        text="👋 Привет! Для вызова такси укажите условия поездки: Стоимость, Точки начала и конца маршрута",
        reply_markup=taxi_keyboards
    )


def taxi_call(call: CallbackQuery):
    """Отправка водителям оповещения о вызове такси"""
    _, ride_id = call.data.split("_")
    ride = Ride.objects.get(pk=ride_id)

    if ride.adress_start == "Не выбрано" or ride.adress_end == "Не выбрано":
        bot.send_message(text="Точки начала и конца поездки не могут быть пустыми!", chat_id=call.message.chat.id)
        call_taxi(call.message, status=1, pk_=ride.pk)
        return

    ride.is_active = True
    ride.save()

    drivers = User.objects.filter(is_driver=True)

    for driver in drivers:
        markup = InlineKeyboardMarkup()
        btn_yes = InlineKeyboardButton(text="✅ Принять заказ!", callback_data=f"ride_accept_{ride.pk}_{driver.pk}")
        btn_no = InlineKeyboardButton(text="❌ Отклонить заказ!", callback_data=f"ride_decline_{ride.pk}_{driver.pk}")
        markup.add(btn_yes).add(btn_no)

        bot.send_message(text=f"""
🚖 Новый заказ для тебя!

👤 Клиент: {ride.user.name} (рейтинг ⭐ {ride.user.rating})  
📍 Маршрут: {ride.adress_start} до {ride.adress_end}
💰 Стоимость поездки: {ride.cost} ₽""",
                         reply_markup=markup,
                         chat_id=driver.telegram_id,
                         )


def answer_ride(call: CallbackQuery):
    """Ответ на заказ такси"""
    _, answer, ride_pk, driver_id = call.data.split("_")
    if answer == "decline":
        return
    else:
        ride = Ride.objects.get(pk=ride_pk)
        driver = User.objects.get(pk=driver_id)
        ride.driver = driver

        ride.save()

        markup = InlineKeyboardMarkup()
        btn = InlineKeyboardButton(text="Я на месте!", callback_data=f"here_{ride.pk}")
        markup.add(btn)

        bot.send_message(chat_id=driver.telegram_id,
                         text=f"Вы приняли заказ!\n\nАдрес: {ride.adress_start}\n\nТелефон клиента:{ride.user.number}\n\nКогда будете на месте - нажмите кнопку ниже!",
                         reply_markup=markup
                         )  # Сообщение водителю о начале поездки
        bot.send_message(chat_id=ride.user.telegram_id,
                         text=f"Ваш заказ принят, ожидайте водителя\n\n🚕 Водитель: {driver.name} (рейтинг ⭐ {driver.rating}\n\nНомер телефона: {driver.number}")  # Сообщение пользователю о принятии поездки


def here_notification(call: CallbackQuery):
    """Оповещение пользователю о приехавшем водителе"""
    _, ride_pk = call.data.split("_")
    ride = Ride.objects.get(pk=ride_pk)

    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text="Поездка окончена!", callback_data=f"end_{ride_pk}")
    markup.add(btn)

    bot.send_message(chat_id=ride.user.telegram_id,
                     text=f"Водитель {ride.driver.name} (тел. {ride.driver.number}) на месте! Свяжитесь с ним для более точной информации")
    bot.send_message(chat_id=ride.driver.telegram_id,
                     text=f"Клиент {ride.user.name} (тел. {ride.user.number}) получил оповещение. Ожидайте его!\n\nПо окончании поездки нажмите кнопку ниже",
                     reply_markup=markup)


def get_rating(call: CallbackQuery):
    """Оценка пассажира и водителя"""
    _, ride_pk = call.data.split("_")
    ride = Ride.objects.get(pk=ride_pk)

    markup_user = InlineKeyboardMarkup()
    star_5 = InlineKeyboardButton(text="")
    star_4 =
    star_3 =
    star_2 =
    star_1 =

    bot.send_message(chat_id=ride.user.telegram_id,
                     text=f"Поездка окончена! Пожалуйста оцените водителя {ride.driver.name}")
    bot.send_message(chat_id=ride.driver.telegram_id,
                     text=f"Поездка окончена! Пожалуйста оцените клиента {ride.driver.name}",
                     reply_markup=markup)