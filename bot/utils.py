import sqlite3
import json
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config.config import MERCADO_PAGO_ACCESS_TOKEN, GOOGLE_API_KEY
import mercadopago
import google.generativeai as genai
from telegram.error import NetworkError, RetryAfter, TimedOut, BadRequest

# Setup Mercado Pago
sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)

# Setup Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

# Setup SQLite
conn = sqlite3.connect('data/interactions.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user_interactions (user_id INTEGER PRIMARY KEY, interactions INTEGER, paid BOOLEAN)''')
conn.commit()

def get_user_interactions(user_id):
    c.execute('SELECT interactions FROM user_interactions WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    if row:
        return row[0]
    else:
        c.execute('INSERT INTO user_interactions (user_id, interactions, paid) VALUES (?, 0, 0)', (user_id,))
        conn.commit()
        return 0

def increment_user_interactions(user_id):
    interactions = get_user_interactions(user_id) + 1
    c.execute('UPDATE user_interactions SET interactions = ? WHERE user_id = ?', (interactions, user_id))
    conn.commit()

def reset_user_interactions(user_id):
    c.execute('UPDATE user_interactions SET interactions = 0, paid = 0 WHERE user_id = ?', (user_id,))
    conn.commit()

def store_user_data(update: Update):
    user = update.message.from_user
    user_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'last_interaction': update.message.date.strftime("%Y-%m-%d %H:%M:%S"),
        'language_code': user.language_code,
        'chat_id': update.effective_chat.id,
        'chat_type': update.effective_chat.type,
        'message_content': update.message.text or update.message.caption,
    }
    with open('data/user_data.json', 'a', encoding='utf-8') as file:
        json.dump(user_data, file, ensure_ascii=False, indent=2)
        file.write('\n')

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

def generate_agronomic_response(question):
    try:
        response = gemini_model.generate_content(question)
        clean_response = clean_markdown_entities(response.text)
        return clean_response
    except Exception as e:
        return f"Lo siento, hubo un error al procesar tu solicitud: {str(e)}"

def clean_markdown_entities(text):
    text = re.sub(r'(?<!\\)([_*`[\]])', r'\\\1', text)
    return text
