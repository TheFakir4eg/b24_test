from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage  # Новый путь для MemoryStorage
from aiogram.client.default import DefaultBotProperties  # Импортируем DefaultBotProperties

import config

# Инициализация хранилища состояний
storage = MemoryStorage()

# Инициализация бота с указанием ParseMode
bot = Bot(token=config.token, 
          default=DefaultBotProperties(parse_mode=ParseMode.HTML)
          )

# Инициализация диспетчера с хранилищем состояний
dispatcher = Dispatcher(storage=storage)