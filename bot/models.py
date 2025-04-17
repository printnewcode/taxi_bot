from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, verbose_name="Имя пользователя телеграмм")
    name = models.CharField(max_length=100, verbose_name="Имя и фамилия человека")
    number = models.CharField(max_length=20, verbose_name="Номер телефона человека", null=True, blank=True)
    telegram_id = models.CharField(max_length=100, verbose_name="Телеграмм айди человека")
    rating = models.FloatField(verbose_name="Рейтинг", null=True, blank=True)

    is_driver = models.BooleanField(default=False, verbose_name="Является ли водителем", null=True, blank=True)
    is_user = models.BooleanField(default=False, verbose_name="Является ли пользователем", null=True, blank=True)
    is_admin = models.BooleanField(default=False, verbose_name="Является ли администратором", null=True, blank=True)

    def __str__(self):
        return str(self.telegram_id)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Ride(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    driver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=False, verbose_name="Статус поездки", null=True, blank=True)
    cost = models.CharField(max_length=100, verbose_name="Стоимость поездки", default="100", null=True, blank=True),
    adress_start = models.CharField(max_length=100, verbose_name="Адрес начала поездки", default="Не выбрано",
                                    null=True, blank=True),
    adress_end = models.CharField(max_length=100, verbose_name="Адрес конца поездки", default="Не выбрано", null=True,
                                  blank=True)
    pay_type = models.CharField(
        max_length=50,
        verbose_name="Тип оплаты",
        default="Не выбрано",
        choices=[("money", "Наличными"), ("payment_transfer", "Переводом")],
        null=True,
        blank=True
    )
