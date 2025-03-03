from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
import bitrix  # Импортируем пакет Bitrix
import asyncio
import config

# Создаем роутер для регистрации обработчиков
router = Router()

# Создаем объект бота
bot = Bot(token=config.token)

# Конфигурация Bitrix API
bitrix_api_instance = bitrix.api  # Используем уже созданный экземпляр из bitrix/api.py

# Обработчик команды /start
@router.message(Command("start"))
async def start(message: Message):
    # Создаем инлайн-клавиатуру с кнопкой "Начать чат"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Начать чат", callback_data="start_chat")]]
    )
    # Отправляем сообщение с кнопкой
    await message.answer("Привет! Нажмите кнопку ниже, чтобы начать чат.", reply_markup=keyboard)

# Обработчик нажатия на инлайн-кнопку
@router.callback_query(F.data == "start_chat")
async def process_callback_start_chat(callback_query: CallbackQuery):
    # Отвечаем на callback
    await callback_query.answer()
    # Отправляем уведомление о начале чата
    await bot.send_message(callback_query.from_user.id, "Чат начат. Вы можете отправлять сообщения.")
    # Уведомляем Bitrix24 о начале чата (создаем лид)
    user_info = {
        'user_id': callback_query.from_user.id,
        'username': callback_query.from_user.full_name
    }
    # Создаем лид для нового пользователя
    lead = bitrix.abstractions.Lead(
        title=f"Telegram User {user_info['user_id']}",
        number=str(user_info['user_id']),
        responsible_id=config.responsible_id,
        name=user_info['username']
    )
    await bitrix_api_instance.add_lead(lead)

# Обработчик входящих текстовых сообщений
@router.message(F.content_type == "text")
async def handle_message(message: Message):
    # Создаем исходящее сообщение для Bitrix24
    outgoing_message = bitrix.abstractions.OutgoingMessage(message)
    # Отправляем сообщение в Bitrix24
    await bitrix_api_instance.send_message(outgoing_message)
    # Подтверждаем получение сообщения
    await message.reply("Сообщение отправлено в службу поддержки.")

# Функция для запуска бота
async def main():
    try:
        # Создаем диспетчер
        dp = Dispatcher()
        # Регистрируем роутер
        dp.include_router(router)
        # Запускаем Bitrix API
        #await bitrix_api_instance.start()
        await bitrix.api.start()
        #asyncio.create_task(bitrix.api.start())
        # Запускаем Telegram бота
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Ошибка при запуске: {e}")

# Запуск скрипта
if __name__ == '__main__':
    asyncio.run(main())