from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

"""Common"""

"""User"""
PAY_TYPE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
money = KeyboardButton(text="Наличными")
payment_transfer = KeyboardButton(text="Переводом")
PAY_TYPE_KEYBOARD.add(money).add(payment_transfer)