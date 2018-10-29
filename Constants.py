import os

HEROKU_URL = os.environ.get("HEROKU_URL")

# Database constants
MONGODB_URI = os.environ.get("MONGODB_URI")

# Telegram API endpoints
TELEGRAM_BASE_API = 'https://api.telegram.org/bot{0}/'  # {0} = bot_token
SEND_MESSAGE_ENDPOINT     = 'sendMessage'            # remember to send with params = chat_id, text
SET_WEBHOOK_ENDPOINT      = 'setWebHook'             # remember to send with params = url
ANSWER_CALLBACK_ENDPOINT  = 'answerCallbackQuery'    # remember to send with params = callback_query_id
EDIT_MESSAGE_ENDPOINT     = 'editMessageText'

# Telegram constants
BOT1_TOKEN = os.environ.get("TOKEN_BOT1","")             # Interative bot
BOT2_TOKEN = os.environ.get("TOKEN_BOT2","")             # Simple bot
BOT1_BASE_API = TELEGRAM_BASE_API.format(BOT1_TOKEN)
BOT2_BASE_API = TELEGRAM_BASE_API.format(BOT2_TOKEN)

# Dados abertos API endpoints
DADOS_ABERTOS_BASE_API = 'https://dadosabertos.camara.leg.br/api/v2/'
PROPOSICOES_ENDPOINT = 'proposicoes'

# BUTTONS CALLBACK DATA
CALLBACK_SHOW_PROPOSITION  = "CALLBACK_SHOW_PROPOSITION"
CALLBACK_SHOW_PROP_EXAMPLE = "CALLBACK_SHOW_PROP_EXAMPLE"