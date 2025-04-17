from functools import wraps

from bot import bot
from bot.models import User, Ride


def drvier_permission(func):
    """
    Checking user for is_driver.
    """

    @wraps(func)
    def wrapped(message) -> None:
        user_id = message.from_user.id
        user = User.objects.get(user_id=user_id)
        if not user.is_driver:
            bot.send_message(user_id,
                             "У вас нет доступа к этой функции! Вы не водитель")
            return
        return func(message)

    return wrapped
