from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bot.handlers import handle_agronomic_question, handle_message, handle_image
from config.config import TELEGRAM_BOT_TOKEN
from bot.terms import terms, start

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("terms", terms))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_agronomic_question))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.photo, handle_image))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
