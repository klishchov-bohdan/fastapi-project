from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Sign up', callback_data='sign-up'),
                                        InlineKeyboardButton(text='Sign in', callback_data='sign-in'),
                                    ],
                                ])

email_confirmation_kb = InlineKeyboardMarkup(row_width=2,
                                             inline_keyboard=[
                                                 [
                                                     InlineKeyboardButton(text='Confirm', callback_data='confirm-email-update'),
                                                     InlineKeyboardButton(text='Cancel', callback_data='cancel-email-update'),
                                                 ],
                                             ])
