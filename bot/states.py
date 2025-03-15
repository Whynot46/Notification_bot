from aiogram.fsm.state import StatesGroup, State


# Регистрация
class Register_steps(StatesGroup):
    fullname = State()  # ФИО


class Notification_create_steps(StatesGroup):
    title = State()
    description = State()
    sender_date = State()
    sender_time = State()
    is_repeat = State()
    sender_weekday = State()
    recipient_type = State()
    recipients_ids = State()