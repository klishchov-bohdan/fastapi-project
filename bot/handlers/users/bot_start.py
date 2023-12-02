import re
import random

import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from data import config
from loader import dp

from filters import IsPrivate
from states import SignIn, SignUp, AdminMe, UpdateEmail
from utils.misc import rate_limit

from keyboards.inline import ikb_menu, email_confirmation_kb

from utils.misc.helpers import is_authenticated_check

from utils import new_redis_conn


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), CommandStart())
async def command_start(message: types.Message):
    try:
        if await is_authenticated_check(message.from_user.id):
            await message.answer(f'Greetings, {message.from_user.first_name}. You already authenticated and can admin your data with this bot. Enter /admin')
        else:
            await message.answer(f'Greetings, {message.from_user.first_name}', reply_markup=ikb_menu)
    except Exception as ex:
        print(ex)
        await message.answer('something went wrong')


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/admin')
async def command_admin(message: types.Message):
    try:
        if await is_authenticated_check(message.from_user.id):
            await message.answer('Enter what you wanna do')
            await AdminMe.message.set()
        else:
            await message.answer(f'Greetings, {message.from_user.first_name}. Please, sign in firstly', reply_markup=ikb_menu)
    except Exception as ex:
        print(ex)
        await message.answer('something went wrong')


@dp.message_handler(state=AdminMe.message)
async def predict_action(message: types.Message, state: FSMContext):
    try:
        with new_redis_conn() as client:
            token = client.get(f'{message.from_user.id}')
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token.decode("utf-8")}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        params = {
            'message': f'{message.text}',
        }
        async with aiohttp.ClientSession() as session:
            async with session.post('http://127.0.0.1:9999/chat/get-gpt-answer', headers=headers, params=params) as response:
                if response.status == 200:
                    if (await response.json())["message"] == 'error':
                        await message.answer('Error prediction')
                    elif (await response.json())["message"] == 'var_error':
                        await message.answer('Error value')
                    elif (await response.json())["message"] == 'show|my_profile|':
                        with new_redis_conn() as client:
                            token = client.get(f'{message.from_user.id}')
                            headers = {
                                'accept': 'application/json',
                                'Authorization': f'Bearer {token.decode("utf-8")}',
                            }
                            async with aiohttp.ClientSession() as session:
                                async with session.get('http://127.0.0.1:9999/users/me', headers=headers) as response:
                                    if response.status == 200:
                                        json = await response.json()
                                        await message.answer(f'username: {json["username"]}\n'
                                                             f'email: {json["email"]}\n'
                                                             f'is admin: {json["is_admin"]}\n'
                                                             f'verified: {json["verified"]}')
                                    else:
                                        await message.answer('Something went wrong')
                    elif (await response.json())["message"].split('|')[0:2] == ['update', 'email']:
                        email = (await response.json())["message"].split("|")[2]
                        await message.answer(f'Update email to {email}?', reply_markup=email_confirmation_kb)
                        # await UpdateEmail.email.set()
                        with new_redis_conn() as client:
                            client.set(f'email_{message.from_user.id}', email)
                    elif (await response.json())["message"].split('|')[0:2] == ['update', 'username']:
                        await message.answer(f'Update username to {(await response.json())["message"].split("|")[2]}?')
                    else:
                        await message.answer('I dont understand')
                else:
                    await message.answer('Error')
                    await state.finish()
    except Exception as ex:
        print(ex)
        await message.answer('something went wrong')
    finally:
        await state.finish()


@dp.callback_query_handler(text='cancel-email-update')
async def confirm_email_update(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Canceled')


@dp.callback_query_handler(text='confirm-email-update')
async def confirm_email_update(call: CallbackQuery, state: FSMContext):
    try:
        with new_redis_conn() as client:
            token = client.get(f'{call.from_user.id}')
            email = client.get(f'email_{call.from_user.id}')
            client.delete(f'email_{call.from_user.id}')
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token.decode("utf-8")}',
        }

        params = {
            'new_email': f'{email.decode("utf-8")}',
        }
        async with aiohttp.ClientSession() as session:
            async with session.patch('http://127.0.0.1:9999/users/me/email', headers=headers, params=params) as response:
                print(await response.text())
                if response.status == 200:
                    await call.message.answer('Success')
                else:
                    await call.message.answer('Error')
    except Exception as ex:
        print(ex)
        await call.message.answer('something went wrong')
    finally:
        await state.finish()

#
# @dp.message_handler(state=SignIn.email)
# async def email_state(message: types.Message, state: FSMContext):
#     answer = message.text
#     regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
#     if re.fullmatch(regex, answer):
#         await state.update_data(email=answer)
#         await message.answer(f'Password:')
#         await SignIn.password.set()
#     else:
#         await message.answer('Невалидный email')


@dp.message_handler(state=SignIn.password)
async def sign_in_password(message: types.Message, state: FSMContext):
    answer = message.text
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': '',
        'username': f'{message.from_user.username}',
        'password': answer,
        'scope': 'me',
        'client_id': f'{message.from_user.id}',
        'client_secret': '',
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:9999/auth/token', headers=headers, data=data) as response:
            if response.status == 200:
                with new_redis_conn() as client:
                    client.set(f'{message.from_user.id}', f'{(await response.json())["access_token"]}')
                await message.answer('Success')
            else:
                await message.answer('Error')
    await state.finish()


@dp.message_handler(state=SignUp.password)
async def sign_up_password(message: types.Message, state: FSMContext):
    s = dp.current_state(user=message.from_user.id)
    await s.update_data(password=message.text)
    await message.answer('Enter email:')
    await SignUp.email.set()


@dp.message_handler(state=SignUp.email)
async def sign_up_email(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        password = data.get('password')
        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
        }

        params = {
            'username': f'{message.from_user.username}',
            'email': f'{message.text}',
            'password': f'{password}',
        }
        async with aiohttp.ClientSession() as session:
            async with session.post('http://127.0.0.1:9999/users/registrate', headers=headers, params=params) as response:
                if response.status == 200:
                    data = {
                        'grant_type': '',
                        'username': f'{message.from_user.username}',
                        'password': f'{password}',
                        'scope': 'me',
                        'client_id': f'{message.from_user.id}',
                        'client_secret': '',
                    }
                    async with session.post('http://127.0.0.1:9999/auth/token', headers=headers, data=data) as response:
                        if response.status == 200:
                            with new_redis_conn() as client:
                                client.set(f'{message.from_user.id}', f'{(await response.json())["access_token"]}')
                            await message.answer('Success')
                        else:
                            await message.answer('Error')
                else:
                    await message.answer('Cant registrate')
    except Exception as ex:
        print(ex)
        await message.answer('Something went wrong')
    finally:
        await state.finish()


@dp.callback_query_handler(text='sign-in')
async def sign_in(call: CallbackQuery):
    if not await is_authenticated_check(call.from_user.id):
        await call.message.answer('Enter your password:')
        await SignIn.password.set()
    else:
        await call.answer('Already signed in')


@dp.callback_query_handler(text='sign-up')
async def sign_up(call: CallbackQuery):
    if not await is_authenticated_check(call.from_user.id):
        await call.message.answer(f'Create new password for this account:')
        await SignUp.password.set()
    else:
        await call.answer('Already signed in')


