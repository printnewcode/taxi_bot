from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import bot
from bot.texts import START_TEXT
from bot.models import User, Ride
from bot.utils import drvier_permission


def menu_driver(user):
    """Меню для водителя"""
    bot.send_message(
        user.telegram_id,
        f"👋 Привет, {user.name}!\n\n"
        f"💼 Ваша роль: Водитель\n"
        f"⭐ Рейтинг: {user.rating}",
    )


@drvier_permission
def get_orders(message: Message):
    """Просмотр всех заказов"""
    driver = User.objects.get(telegram_id=message.chat.id)
    if Ride.objects.filter(driver=driver) & Ride.objects.filter(is_active=True) is not None:
        bot.send_message(text="У вас уже есть активный заказ")
        menu_driver(user=driver)
        return

    orders = (Ride.objects.filter(is_active=True) & Ride.objects.filter(driver__isnull=True))
    markup = InlineKeyboardMarkup()
    for order in orders:
        btn = InlineKeyboardButton(text=f"Заказ {order.pk}", callback_data=f"orders_{order.pk}_{message.chat.id}")
        markup.add(btn)

    bot.send_message(chat_id=message.chat.id, text="Вот список всех доступных заказов:", reply_markup=markup)


def get_order(call: CallbackQuery):
    """Просмотр информации о доступном заказе"""
    _, ride_pk, driver_id = call.data
    ride = Ride.objects.get(pk=ride_pk)

    markup = InlineKeyboardMarkup()
    btn_yes = InlineKeyboardButton(text="✅ Принять заказ!", callback_data=f"ride_accept_{ride.pk}_{driver_id}")
    btn_no = InlineKeyboardButton(text="❌ Отклонить заказ!", callback_data=f"ride_decline_{ride.pk}_{driver_id}")
    markup.add(btn_yes).add(btn_no)

    bot.send_message(text=f"""
    🚖 Новый заказ для тебя!

    👤 Клиент: {ride.user.name} (рейтинг ⭐ {ride.user.rating})  
    📍 Маршрут: {ride.adress_start} до {ride.adress_end}
    💰 Стоимость поездки: {ride.cost} ₽""",
                     reply_markup=markup,
                     chat_id=call.message.chat.id,
                     )


