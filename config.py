# Токен бота, получаемый у @BotFather
token: str = '7614300683:AAHl8_LJJblecVFk7k2nzWEBCDA1h0hzZIQ'
# '7811978605:AAHVFJWvZKc41l_eU-JZr17-ZwZkvoOByqE' #sanatoriy_don_bot
# '7614300683:AAHl8_LJJblecVFk7k2nzWEBCDA1h0hzZIQ' #fakir_test_bot

# Относительный путь до базы данных из корня проекта (можно не менять)
#db_path: str = 'bot.db'

# Время (в секундах) до отправки финального сообщения
time_before_question: int = 60


# Конфигурация сервера (отдельно для каждого бота)
# URL, запросы с которого буду пробрасываться в ВМ (с указанием порта!)
host_url: str = 'http://tg-bot.alpha.local:59995'

# Адрес ВМ в локальной сети
host: str = '10.6.1.48'

# Порт, на который пробрасываются запросы
port: int = 59995


# Bitrix API
# Путь до api-сервера битрикса (не менять)
api_url: str = 'https://dev-portal.olimp03.ru/rest'

# ID пользователя Битрикс, которому будут падать лиды
responsible_id: int = 14454

# Время обновления (в секундах) токена OAuth (можно не менять, не более 3600)
token_update_time: int = 3000

# Путь до OAuth сервера Битрикс (не менять)
token_update_url: str = 'https://oauth.bitrix.info/oauth/token'

# Полученные данные при создании приложения в Битриксе
# https://dev-portal.olimp03.ru - Разработчикам - Интеграции - (19) Локальное приложение
client_id: str = 'local.67b70f659197a1.62317106'
client_secret: str = 'PxHrt5C8LNtiKe8JwycmAHNPNCIDjiibIafrb52yqptZ7QnQkc'

# ID открытой линии Битрикс (не менять)
ol_id: int = 259

# ID коннектора Битрикс (отдельно для каждого бота)
connector_id: str = 'tmm_bot_connector'

# Отображаемое имя коннектора Битрикс
connector_name: str = 'ScandyBot'

# Картинка коннектора Битрикс (DATA-представление иконки SVG)
connector_pic: str = '/'
