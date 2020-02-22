import telegram
from telegram.ext import Updater

bot = telegram.Bot(token="ENTER_YOUR_TOKEN_HERE")
updater = Updater(token="ENTER_YOUR_TOKEN_HERE", use_context=True)
