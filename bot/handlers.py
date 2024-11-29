from telegram import Update
from telegram.ext import CallbackContext
from .utils import store_user_data, create_payment_button, get_user_interactions, increment_user_interactions, generate_agronomic_response
from .image_processing import process_image


def handle_agronomic_question(update: Update, context: CallbackContext):
    user = update.message.from_user
    question = update.message.text
    response = generate_agronomic_response(question)
    update.message.reply_text(response, parse_mode='Markdown')
    store_user_data(update)


def handle_message(update: Update, context: CallbackContext):
    user = update.message.from_user
    interactions = get_user_interactions(user.id)
    if interactions >= 100:
        create_payment_button(update, context)
    else:
        increment_user_interactions(user.id)
        update.message.reply_text(f"Hola {user.first_name}, proporcióname una imagen de tu hoja o follaje para cuantificar el contenido de clorofila.🌱")
    store_user_data(update)


def handle_image(update: Update, context: CallbackContext):
    user = update.message.from_user
    interactions = get_user_interactions(user.id)
    if interactions >= 100:
        create_payment_button(update, context)
    else:
        increment_user_interactions(user.id)
        store_user_data(update)
        process_image(update, context)
