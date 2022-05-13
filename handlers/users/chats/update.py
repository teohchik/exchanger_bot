import logging

from aiogram.types import CallbackQuery
from sqlalchemy.orm import sessionmaker

from keyboards.default.cancel import cancel_menu
from keyboards.inline.chats.callback_datas import chats_button_callback, select_update_chat_buttons_callback, \
    select_update_group_buttons_callback
from keyboards.inline.chats.select_group_update import select_update_group_buttons
from keyboards.inline.chats.select_update_chat import select_update_chat_buttons
from keyboards.inline.groups.callback_datas import groups_button_callback
from keyboards.inline.groups.delete_groups import delete_group_buttons
from loader import dp
from states.groups.new_group_state import NewGroupOrderState
from utils.db_api.models import engine, Group, Chat


@dp.callback_query_handler(select_update_chat_buttons_callback.filter(type_command='select_update_chat'))
async def chat_buttons_call(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    pk = callback_data.get('pk')

    await call.message.answer('В какую группу присвоить чат?', reply_markup=await select_update_group_buttons(pk))


@dp.callback_query_handler(select_update_group_buttons_callback.filter(type_command='select_group'))
async def chat_buttons_call(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    pk_group = callback_data.get('pk_group')
    pk_chat = callback_data.get('pk_chat')

    session = sessionmaker(bind=engine)()
    chat = session.query(Chat).get(pk_chat)
    chat.group_id = pk_group
    session.add(chat)
    session.commit()

    await call.message.answer(f'Чату "{chat.title}" была присвоина группа {chat.group.title}')
    await call.message.delete()
    logging.info(f'Чату "{chat.title}" была присвоина группа {chat.group.title}')
    session.close()