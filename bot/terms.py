from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

def terms(update: Update, context: CallbackContext):
    terms_message = (
        "**Términos y Condiciones:**\n"
        "1. Al usar este bot, aceptas los términos y condiciones de nuestro servicio.\n"
        "2. El análisis de clorofila es orientativo y no sustituye la asesoría profesional.\n"
        "3. Los datos proporcionados serán tratados con confidencialidad y según nuestra política de privacidad.\n"
        "4. El uso del bot está limitado a 10 interacciones gratuitas, después de lo cual se requiere una suscripción.\n"
        "5. Para más detalles, visita nuestra página de términos y condiciones."
    )
    update.message.reply_text(terms_message, parse_mode='Markdown')

def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    welcome_message = (
        f"Hola {user.first_name}, ¿has sido testigo de un delito?"
        "Envía evidencia del delito y contribuye a la seguridad colombiana"
        "**Términos y Condiciones:**\n"
        "1. Al usar este bot, aceptas los términos y condiciones de nuestro servicio.\n"
        "3. Los datos proporcionados serán tratados con confidencialidad y según nuestra política de privacidad.\n"
        "5. Para más detalles, visita nuestra página de términos y condiciones."
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message, parse_mode='Markdown')
