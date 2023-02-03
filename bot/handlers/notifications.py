from decimal import Decimal, InvalidOperation

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from flag import flag

from controllers.notification import NotificationController
from services.exchange_rate import get_current_exchange_rate
from services.utils import get_dict_flag_currencies, get_list_flag_currencies
from states.notification import AddNotificationState, RemoveNotificationState


async def actions_cancel(message: types.Message, state: FSMContext):
    """Canceling the notification addition process"""
    await state.finish()
    await message.answer('You canceled the operation', reply_markup=types.ReplyKeyboardRemove())


async def add_notification(message: types.Message, state: FSMContext):
    """Starting the process of adding a new notification"""
    # NOTE Добавить логи
    flag_currencies_list = await get_list_flag_currencies()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*flag_currencies_list)
    await message.answer('Select the currency for which you want to set the notification', reply_markup=keyboard)
    await state.set_state(AddNotificationState.waiting_for_currency_selection.state)


async def currency_chosen(message: types.Message, state: FSMContext):
    """User's choice of the currency at which the notification will be received"""
    flag_currencies_list = await get_list_flag_currencies()
    emoji_currency = message.text.lower()
    if emoji_currency not in flag_currencies_list:
        await message.answer('Please select the currency using the keyboard below')
        return
    # NOTE Можно заменить на один метод get_dict_flag_currencies с ключом
    flag_currencies_dict = await get_dict_flag_currencies()
    currency_char = flag_currencies_dict[emoji_currency]
    await state.update_data(chosen_currency_char=currency_char, chosen_currency_flag=emoji_currency)
    await state.set_state(AddNotificationState.waiting_for_value_input.state)
    await message.answer('Enter the value at which you need to be notified', reply_markup=types.ReplyKeyboardRemove())


async def value_chosen(message: types.Message, state: FSMContext):
    """Setting by the user the currency value at which the notification will be received"""
    # NOTE Добавить клавиатуру с числами (точка запятая)
    try:
        user_value = Decimal(message.text).quantize(Decimal('1.0000'))
    except (ValueError, InvalidOperation):
        await message.answer('Please enter the correct value of the number')
        return
    if user_value <= 0:
        await message.answer('Please enter the correct value of the number')
        return
    user_data = await state.get_data()
    current_exchange_rate = await get_current_exchange_rate()
    currency_char = user_data.get('chosen_currency_char')
    current_value = getattr(current_exchange_rate.valute, currency_char).value
    # NOTE Не работает сравнение decimal.Decimal и float
    if current_value == user_value:
        await message.answer('The value you specified has already been reached at the moment')
        await state.finish()
        return
    comparison_sign = '<' if current_value > user_value else '>'
    await NotificationController.create(
        user_id=message.from_user.id,
        currency_char_code=currency_char,
        value=user_value,
        comparison_sign=comparison_sign,
    )
    await message.answer(
        f"""A notification for the value of {user_value} {user_data.get('chosen_currency_flag')} currency has been added.\n\n"""
        'You will receive a notification when the specified currency reaches this value'
    )
    await state.finish()


async def list_notification(message: types.Message):
    """Output of all notifications"""
    notifications = await NotificationController.get_all_user_notifications(message.from_user.id)
    if not notifications:
        await message.reply("""You have not yet had any notifications created""")
        return
    current_exchange_rate = await get_current_exchange_rate()
    data = ''
    for index, notification in enumerate(notifications, start=1):
        user_value = notification.value
        currency_char = notification.currency_char_code
        current_value = getattr(current_exchange_rate.valute, currency_char).value
        data += f'{index}. {flag(currency_char[:2])} {user_value} - current value: {current_value}\n'
    await message.reply('List your notifications:\n\n' + data)


async def remove_notification(message: types.Message, state: FSMContext):
    """Deleting the user's notifications"""
    # NOTE Одинаковый код вынести в отдельный метод
    notifications = await NotificationController.get_all_user_notifications(message.from_user.id)
    current_exchange_rate = await get_current_exchange_rate()
    data = ''
    for index, notification in enumerate(notifications, start=1):
        user_value = notification.value
        currency_char = notification.currency_char_code
        current_value = getattr(current_exchange_rate.valute, currency_char).value
        data += f'{index}. {flag(currency_char[:2])} {user_value} - current value: {current_value}\n'

    index_with_notification = {str(index): notification for index, notification in enumerate(notifications, start=1)}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*index_with_notification.keys())
    await message.answer('List your notifications:\n\n' + data)
    await message.answer('Enter the notification number to delete it', reply_markup=keyboard)
    await state.update_data(index_with_notification=index_with_notification)
    await state.set_state(RemoveNotificationState.waiting_for_index_input.state)


async def index_chosen(message: types.Message, state: FSMContext):
    """User's choice of the notification number that he wants to delete"""
    user_data = await state.get_data()
    index_with_notification = user_data.get('index_with_notification')
    if message.text not in index_with_notification.keys():
        await message.answer('Please select the index using the keyboard below')
        return
    await NotificationController.delete(index_with_notification.get(message.text))
    await message.answer('The notification has been deleted', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def remove_all_notification(message: types.Message):
    await message.answer('List of available commands:\n\n')
    # Вывести клавиатуру с подтверждением удаления всех уведомлений (да/нет)

    # При нажатии на да - удалить все записи уведомлений пользователя

    # При нажатии на нет - сбросить состояние и ничего не делать


def register_handlers_notification(dp: Dispatcher):
    dp.register_message_handler(actions_cancel, commands='cancel', state='*')
    dp.register_message_handler(actions_cancel, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(add_notification, commands='add_notification', state='*')
    dp.register_message_handler(currency_chosen, state=AddNotificationState.waiting_for_currency_selection)
    dp.register_message_handler(value_chosen, state=AddNotificationState.waiting_for_value_input)
    dp.register_message_handler(list_notification, commands='list_notification')
    dp.register_message_handler(remove_notification, commands='remove_notification', state='*')
    dp.register_message_handler(index_chosen, state=RemoveNotificationState.waiting_for_index_input)
    dp.register_message_handler(remove_all_notification, commands='remove_all_notification')