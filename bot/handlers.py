from aiogram.filters.command import Command
from aiogram import F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER, KICKED, LEFT, RESTRICTED, ADMINISTRATOR, CREATOR
from aiogram.enums import ChatType
import bot.keyboards as kb
import bot.database as db
from bot.states import *
from bot.logger import error_handler, logger
from bot.config import Config
import re
import ast


router = Router()


@error_handler
@router.message(F.text, Command("start"))
async def start_loop(message: Message, state: FSMContext):
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await db.add_group(message.chat.id, message.chat.title)
        try:
            await message.answer(f"Всем привет! Я - гномик Стёпа, местный звонарь 🧙🏻‍♂️\nВы добавили меня в эту группу, а значит теперь я смогу отправлять сюда напоминания, которые вы создадите в чате со мной!")
        except Exception as error:
            logger.error(f"Ошибка при отправке сообщения в группу {message.chat.title}: {error}", exc_info=True)
    else:
        await message.answer("Я слышу утренний колокол, он бесов дразнит... 😜\n"
                            "Добро пожаловать в панель управления колокольней Роутима ⛪️\n"
                            "Я - гномик Стёпа, местный звонарь 🧙🏻‍♂️\n"
                            "Именно я навожу по утрам суету в Роутиме, пробуждая от сна зазевавшихся менеджеров и напоминая о необходимости оценить неведомое ТЗ 🙂")
        if not await db.is_old(message.from_user.id):
            await state.set_state(Register_steps.fullname)
            await message.answer("Для начала давай познакомимся, моё имя ты уже знаешь.\nВведи своё ФИО:")
        else:
            user_fullname = await db.get_fullname(message.from_user.id)
            await message.answer(f"Приветствую Вас, {user_fullname}!", reply_markup=await kb.get_main_menu_keyboard(message.from_user.id))


@router.message(Register_steps.fullname)
async def registration(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    register_data = await state.get_data()
    if re.match(r"^[А-ЯЁа-яёA-Za-z]+(?:-[А-ЯЁа-яёA-Za-z]+)?\s[А-ЯЁа-яёA-Za-z]+(?:-[А-ЯЁа-яёA-Za-z]+)?\s[А-ЯЁа-яёA-Za-z]+(?:-[А-ЯЁа-яёA-Za-z]+)?$", message.text):
        lastname, firstname, middlename = (register_data["fullname"]).split(" ")
        if await db.is_register(firstname, middlename, lastname):
            await db.update_user_id(message.from_user.id, firstname, middlename, lastname)
            await message.answer(f"Приветствую Вас, {register_data['fullname']}!", reply_markup=await kb.get_main_menu_keyboard(message.from_user.id))
            await state.clear()
        else:
            await message.answer("Мой руководитель не вводил тебя в свой справочник 😑")
    else:
        await message.answer("😬 Некорректный формат ФИО!")
        await state.set_state(Register_steps.fullname)
        await message.answer("Введи своё ФИО:")


@router.message(F.text == "🏠Напоминания Роутима")
async def get_routeam_notifications(message: Message):
    if Config.is_admin(message.from_user.id):
        notifications_dict = await db.get_all_notifications()
        if len(notifications_dict) > 0:
            for notification_id, notification_data in notifications_dict.items():
                # Преобразуем строку recipients_ids в словарь
                recipients_ids = ast.literal_eval(notification_data['recipients_ids'])
                
                # Обрабатываем пользователей
                user_ids = recipients_ids.get('users', [])
                user_names = []
                for user_id in user_ids:
                    fullname = await db.get_fullname(user_id)
                    if fullname:
                        user_names.append(fullname)
                
                # Обрабатываем группы
                group_ids = recipients_ids.get('groups', [])
                group_names = []
                for group_id in group_ids:
                    group_name = await db.get_group_name(group_id)
                    if group_name:
                        group_names.append(group_name)
                
                # Формируем строку с получателями
                recipients_str = ""
                if user_names:
                    recipients_str += f"Пользователи: {', '.join(user_names)}\n"
                if group_names:
                    recipients_str += f"Группы: {', '.join(group_names)}\n"
                
                # Формируем текст напоминания
                notification_text = (
                    f"Напоминание ID: {notification_id}\n"
                    f"Название: {notification_data['title']}\n"
                    f"Описание: {notification_data['description']}\n"
                    f"Дата отправки: {notification_data['sender_date']}\n"
                    f"Время отправки: {notification_data['sender_time']}\n"
                    f"Повторение: {'Да' if notification_data['is_repeat'] else 'Нет'}\n"
                )

                # Добавляем дни недели, если они есть
                if notification_data['sender_weekday'] != "None":
                    notification_text += f"Дни недели: {notification_data['sender_weekday']}\n"

                # Добавляем получателей
                notification_text += f"Получатели: {recipients_str if recipients_str else 'Нет получателей'}"
                
                # Отправляем сообщение с информацией о напоминании
                await message.answer(notification_text, reply_markup=await kb.get_edit_notification_keyboard(notification_id))
        else:
            await message.answer("Ваш верный слуга сидит без работы😔\nВ моём блокноте нет ни одной записи о напоминаниях")


@router.message(F.text == "🧑🏻‍💻Мои напоминания")
async def get_user_notifications(message: Message):
    if Config.is_admin(message.from_user.id):
        notifications_dict = await db.get_author_notifications(message.from_user.id)
        if len(notifications_dict) > 0:
            for notification_id, notification_data in notifications_dict.items():
                recipients_ids = ast.literal_eval(notification_data['recipients_ids'])
                user_ids = recipients_ids.get('users', [])
                user_names = []
                for user_id in user_ids:
                    fullname = await db.get_fullname(user_id)
                    if fullname:
                        user_names.append(fullname)
                
                group_ids = recipients_ids.get('groups', [])
                group_names = []
                for group_id in group_ids:
                    group_name = await db.get_group_name(group_id)
                    if group_name:
                        group_names.append(group_name)
                
                recipients_str = ""
                if user_names:
                    recipients_str += f"{', '.join(user_names)}\n"
                if group_names:
                    recipients_str += f"{', '.join(group_names)}\n"
                
                notification_text = (
                    f"Напоминание ID: {notification_id}\n"
                    f"Название: {notification_data['title']}\n"
                    f"Описание: {notification_data['description']}\n"
                    f"Дата отправки: {notification_data['sender_date']}\n"
                    f"Время отправки: {notification_data['sender_time']}\n"
                    f"Повторение: {'Да' if notification_data['is_repeat'] else 'Нет'}\n"
                )

                if notification_data['sender_weekday'] != "None":
                    notification_text += f"Дни недели: {notification_data['sender_weekday']}\n"

                notification_text += f"Получатели: {recipients_str if recipients_str else 'Нет получателей'}"
                
                await message.answer(notification_text, reply_markup=await kb.get_edit_notification_keyboard(notification_id))
        else:
            await message.answer("У вас нет доступных напоминаний🤔")


@router.message(F.text == "👥Пользователи и группы")
async def get_user_notifications(message: Message, state: FSMContext):
    if Config.is_admin(message.from_user.id):
        users_dict = await db.get_all_users_dict()
        groups_dict = await db.get_all_groups()

        if not users_dict:
            await message.answer("Нет активных пользователей")
        else:
            await message.answer("Пользователи:", reply_markup=await kb.get_users_list_keyboard())

        if not groups_dict:
            await message.answer("Меня нет ещё ни в одной группе")
        else:
            await message.answer("Группы:", reply_markup=await kb.get_groups_list_keyboard())


@router.message(F.text == "🔔Создать напоминание")
async def create_notification(message: Message, state: FSMContext):
    await state.set_state(Notification_create_steps.title)
    await message.answer("Укажите название напоминания", reply_markup=await kb.remove_keyboard())


@router.message(Notification_create_steps.title)
async def set_notification_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Notification_create_steps.description)
    await message.answer("Укажите описание напоминания", reply_markup=await kb.remove_keyboard())


@router.message(Notification_create_steps.description)
async def set_notification_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Notification_create_steps.sender_date)
    await message.answer("Укажите дату напоминания", reply_markup=await kb.remove_keyboard())


@router.message(Notification_create_steps.sender_date)
async def set_notification_sender_date(message: Message, state: FSMContext):
    if re.match(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$", message.text):
        await state.update_data(sender_date=message.text)
        await state.set_state(Notification_create_steps.sender_time)
        await message.answer("Укажите время напоминания", reply_markup=await kb.get_time_keyboard())
    else:
        await state.set_state(Notification_create_steps.sender_date)
        await message.answer("😬 Введите дату в формате ДД.ММ.ГГГГ")


@router.message(Notification_create_steps.sender_time)
async def set_notification_sender_time(message: Message, state: FSMContext):
    if re.match(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$", message.text):
        await state.update_data(sender_time=message.text)
        await state.set_state(Notification_create_steps.is_repeat)
        await message.answer("Нужно ли повторять напоминание?", reply_markup=await kb.get_confirm_keyboard())
    else:
        await state.set_state(Notification_create_steps.sender_time)
        await message.answer("😬 Введите время в формате ЧЧ:ММ")


@router.message(Notification_create_steps.is_repeat)
async def set_notification_repeat(message: Message, state: FSMContext):
    if message.text == "Да":
        await state.update_data(is_repeat=True)
        await state.set_state(Notification_create_steps.sender_weekday)
        await message.answer("Выберите дни недели для еженедельных напоминаний", reply_markup=await kb.get_weekdays_keyboard())
        await message.answer('После выбора нажмите "Продолжить"', reply_markup=await kb.get_continue_keyboard())
    elif message.text == "Нет":
        await state.update_data(is_repeat=False)
        await state.update_data(sender_weekday=None)
        await state.set_state(Notification_create_steps.recipient_type)
        await message.answer("Куда отправить напоминание?", reply_markup=await kb.get_recipient_type_keyboard())
    else:
        await state.set_state(Notification_create_steps.is_repeat)
        await message.answer("Неизвестная команда", reply_markup=await kb.get_confirm_keyboard())


@router.message(Notification_create_steps.sender_weekday, F.text == "Продолжить")
async def handle_weekday_continue(message: Message, state: FSMContext):
    data = await state.get_data()
    selected_weekdays = data.get("selected_weekdays", [])

    if not selected_weekdays:
        await message.answer("Выберите хотя бы один день недели!")
        return

    await state.update_data(sender_weekday=selected_weekdays)

    await state.set_state(Notification_create_steps.recipient_type)
    await message.answer("Куда отправить напоминание?", reply_markup=await kb.get_recipient_type_keyboard())

@router.callback_query(F.data.startswith("weekday_"))
async def handle_weekday_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_weekdays = data.get("selected_weekdays", [])

    weekday = callback.data.split("_")[1]

    if weekday in selected_weekdays:
        selected_weekdays.remove(weekday)
    else:
        selected_weekdays.append(weekday)

    current_keyboard = callback.message.reply_markup.inline_keyboard

    new_keyboard = []
    for row in current_keyboard:
        new_row = []
        for button in row:
            button_text = button.text
            button_data = button.callback_data

            if button_data == f"weekday_{weekday}":
                if weekday in selected_weekdays:
                    button_text = f"{button_text} ✅"
                else:
                    button_text = button_text.replace(" ✅", "")

            new_row.append(InlineKeyboardButton(text=button_text, callback_data=button_data))
        new_keyboard.append(new_row)

    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))

    await state.update_data(selected_weekdays=selected_weekdays)
    await callback.answer()


@router.callback_query(F.data.startswith("notification_user_"))
async def handle_user_selection(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split("_")[2])
    data = await state.get_data()
    selected_users = data.get("selected_users", [])

    # Проверяем, был ли пользователь уже выбран
    if user_id in selected_users:
        selected_users.remove(user_id)  # Убираем пользователя из выбранных
    else:
        selected_users.append(user_id)  # Добавляем пользователя в выбранные

    # Обновляем состояние
    await state.update_data(selected_users=selected_users)

    # Получаем текущую разметку
    current_keyboard = callback.message.reply_markup.inline_keyboard

    # Создаем новую разметку
    new_keyboard = []
    for row in current_keyboard:
        new_row = []
        for button in row:
            button_text = button.text
            button_data = button.callback_data

            # Если это кнопка выбранного пользователя, добавляем/убираем ✅
            if button_data == f"notification_user_{user_id}":
                if user_id in selected_users:
                    button_text = f"{button_text} ✅"
                else:
                    button_text = button_text.replace(" ✅", "")

            new_row.append(InlineKeyboardButton(text=button_text, callback_data=button_data))
        new_keyboard.append(new_row)

    # Проверяем, изменилась ли разметка
    if new_keyboard != current_keyboard:
        await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))
    else:
        # Если разметка не изменилась, просто отвечаем на callback
        await callback.answer()

    await callback.answer()


@router.callback_query(F.data.startswith("notification_group_"))
async def handle_group_selection(callback: CallbackQuery, state: FSMContext):
    group_id = int(callback.data.split("_")[2])
    data = await state.get_data()
    selected_groups = data.get("selected_groups", [])

    if group_id in selected_groups:
        selected_groups.remove(group_id)
    else:
        selected_groups.append(group_id)

    await state.update_data(selected_groups=selected_groups)

    current_keyboard = callback.message.reply_markup.inline_keyboard
    new_keyboard = []
    for row in current_keyboard:
        new_row = []
        for button in row:
            button_text = button.text
            button_data = button.callback_data

            if button_data == f"notification_group_{group_id}":
                if group_id in selected_groups:
                    button_text = f"{button_text} ✅"
                else:
                    button_text = button_text.replace(" ✅", "")

            new_row.append(InlineKeyboardButton(text=button_text, callback_data=button_data))
        new_keyboard.append(new_row)

    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))
    await callback.answer()


@router.message(Notification_create_steps.recipient_type, F.text == "В группу")
async def handle_group_recipient(message: Message, state: FSMContext):
    await state.update_data(recipient_type="В группу")
    await state.set_state(Notification_create_steps.recipients_ids)
    await message.answer("Выберите группы для отправки напоминания", reply_markup=await kb.get_notification_groups_list_keyboard())
    await message.answer('После выбора нажмите "Создать"', reply_markup=await kb.get_create_keyboard())


@router.message(Notification_create_steps.recipient_type, F.text == "В личные сообщения")
async def handle_user_recipient(message: Message, state: FSMContext):
    await state.update_data(recipient_type="В личные сообщения")
    await state.set_state(Notification_create_steps.recipients_ids)
    await message.answer("Выберите пользователей для отправки напоминания", reply_markup=await kb.get_notification_users_list_keyboard())
    await message.answer('После выбора нажмите "Создать"', reply_markup=await kb.get_create_keyboard())
    

@router.callback_query(F.data.startswith("user_"))
async def handle_user_selection(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    if user_id == callback.from_user.id:
        await callback.answer("Вы не можете удалить самого себя")
        return
    await callback.message.edit_reply_markup(reply_markup=await kb.get_user_actions_keyboard(user_id))
    await callback.answer()


@router.callback_query(F.data.startswith("delete_user_"))
async def handle_delete_user(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[2])
    await db.delete_user(user_id)
    await callback.message.edit_reply_markup(reply_markup=await kb.get_users_list_keyboard())
    await callback.answer(f"Пользователь с ID {user_id} удален.")


@router.callback_query(F.data.startswith("spare_user_"))
async def handle_spare_user(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=await kb.get_users_list_keyboard())
    await callback.answer(f"Вы пощадили пользователя с ID {user_id}.")
    

@router.message(Notification_create_steps.recipients_ids, F.text == "Создать")
async def handle_recipients_continue(message: Message, state: FSMContext):
    data = await state.get_data()
    selected_users = data.get("selected_users", [])
    selected_groups = data.get("selected_groups", [])
    recipient_type = data.get("recipient_type", "")

    # Проверяем, что хотя бы один получатель выбран
    if not selected_users and not selected_groups:
        await message.answer("Выберите хотя бы одного получателя!")
        return

    # Обновляем состояние с выбранными получателями
    await state.update_data(recipients_ids={"users": selected_users, "groups": selected_groups})

    # Создаем текст напоминания
    notification_data_str = (
        f"Напоминание {data['title']} успешно создано!\n"
        f"Описание: {data['description']}\n"
        f"Дата отправки: {data['sender_date']}\n"
        f"Время отправки: {data['sender_time']}\n"
    )

    if data['is_repeat']:
        notification_data_str += f"Выбранные дни: {', '.join(data['sender_weekday'])}\n"

    if recipient_type == "В личные сообщения":
        users_names = [await db.get_user_name(user_id) for user_id in selected_users]
        notification_data_str += f"Выбранные пользователи: {users_names}\n"
    elif recipient_type == "В группу":
        group_names = [await db.get_group_name(group_id) for group_id in selected_groups]
        group_names_str = ", ".join(group_names)
        notification_data_str += f"Выбранные группы: {group_names_str}\n"

    # Отправляем сообщение с информацией о напоминании
    await message.answer(notification_data_str, reply_markup=await kb.get_main_menu_keyboard(message.from_user.id))

    # Сохраняем напоминание в базу данных
    await db.add_notification(
        author_id=message.from_user.id,
        title=data['title'],
        description=data['description'],
        sender_date=data['sender_date'],
        sender_time=data['sender_time'],
        is_repeat=data['is_repeat'],
        sender_weekday=data['sender_weekday'],
        recipients_ids={"users": selected_users, "groups": selected_groups},
    )

    # Очищаем состояние
    await state.clear()


@router.callback_query(F.data.startswith("delete_notification_"))
async def handle_delete_notification(callback: CallbackQuery):
    notification_id = int(callback.data.split("_")[2])
    await db.delete_notification(notification_id)
    await callback.answer(f"Напоминание {notification_id} удалено.")
    await callback.message.delete()


    