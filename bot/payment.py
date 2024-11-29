from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import mercadopago
from config.config import MERCADO_PAGO_ACCESS_TOKEN

sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)

def create_payment_button(update: Update, context: CallbackContext):
    preference_data = {
       "items": [
           {
               "title": "ClorofilaBot Analysis",
               "quantity": 1,
               "unit_price": 16.00,
               "currency_id": "USD"
           }
       ]
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    payment_url = preference["init_point"]

    keyboard = [
       [InlineKeyboardButton("Pagar", url=payment_url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
       "Has alcanzado el límite de análisis gratuito. Por favor, realiza el pago para continuar utilizando el servicio.",
       reply_markup=reply_markup
    )
