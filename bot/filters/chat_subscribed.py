from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data import config
from loader import bot, dp


class IsSubscribed(BoundFilter):
    async def check(self, message: types.Message):
        sub = await bot.get_chat_member(chat_id=config.chat_id, user_id=message.from_user.id)
        if sub.status != types.ChatMemberStatus.LEFT:
            return True
        else:
            markup = InlineKeyboardMarkup(row_width=1,
                                          inline_keyboard=[
                                              [
                                                  InlineKeyboardButton(text='Subscribe',
                                                                       url='https://t.me/+AmDIzfUNlCtiZGQy')
                                              ]
                                          ])
            await dp.bot.send_message(chat_id=message.from_user.id,
                                      text=f'Subscribe to telegram chat', reply_markup=markup)
            raise CancelHandler()
