import os
import cv2
import numpy as np
from telegram import Update
from telegram.error import BadRequest
from .utils import generate_agronomic_response
from telegram.ext import CallbackContext
from .injector import injector

model = injector.model
scaler = injector.scaler

def process_image(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id
    user_first_name = user.first_name

    photo_file = update.message.photo[-1].get_file()
    caption = update.message.caption if update.message.caption else ""
    
    # Crear una carpeta para el usuario si no existe
    user_dir = f'data/images/{user_id}'
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    
    # Guardar la imagen en una ruta temporal
    temp_photo_path = 'received_image.jpg'
    photo_file.download(temp_photo_path)

    # Lee la imagen usando OpenCV
    img = cv2.imread(temp_photo_path)

    # Convertir la imagen a espacio de color HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Ajustar un rango para el color verde de las hojas
    lower_green = np.array([25, 40, 25])
    upper_green = np.array([85, 255, 255])

    # Crear una máscara para segmentar la hoja
    mask_hsv = cv2.inRange(hsv, lower_green, upper_green)

    # Aplicar operaciones morfológicas para cerrar pequeños huecos en la segmentación
    kernel = np.ones((5,5), np.uint8)
    mask_hsv_closed = cv2.morphologyEx(mask_hsv, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Encontrar el bounding box de la hoja segmentada
    x, y, w, h = cv2.boundingRect(mask_hsv_closed)

    # Centrar y recortar la imagen
    center_x = x + w // 2
    center_y = y + h // 2
    desired_width, desired_height = 1854, 2635
    x1 = max(0, center_x - desired_width // 2)
    y1 = max(0, center_y - desired_height // 2)
    x2 = min(img.shape[1], center_x + desired_width // 2)
    y2 = min(img.shape[0], center_y + desired_height // 2)

    cropped_img = img[y1:y2, x1:x2]
    resized_img = cv2.resize(cropped_img, (desired_width, desired_height))

    # Continuar con la segmentación de la imagen redimensionada
    hsv_resized = cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV)
    mask_hsv_resized = cv2.inRange(hsv_resized, lower_green, upper_green)
    mask_hsv_closed_resized = cv2.morphologyEx(mask_hsv_resized, cv2.MORPH_CLOSE, kernel, iterations=2)
    segmented_leaf_hsv_resized = cv2.bitwise_and(resized_img, resized_img, mask=mask_hsv_closed_resized)

    # Extraer valores medianos de RGB
    red_median = np.median(segmented_leaf_hsv_resized[:, :, 2][mask_hsv_closed_resized == 255])
    green_median = np.median(segmented_leaf_hsv_resized[:, :, 1][mask_hsv_closed_resized == 255])
    blue_median = np.median(segmented_leaf_hsv_resized[:, :, 0][mask_hsv_closed_resized == 255])

    input_features = np.array([[red_median, green_median, blue_median]])

    # Escalar las características usando el escalador cargado
    input_features_scaled = scaler.transform(input_features)

    # Hacer la predicción
    spad_prediction = model.predict(input_features_scaled)[0]

    # Guardar la imagen resultante con el nombre result_dato.jpg en la carpeta del usuario
    result_photo_path = os.path.join(user_dir, f'result_{spad_prediction:.2f}.jpg')
    cv2.imwrite(result_photo_path, resized_img)

    # Eliminar la imagen temporal
    os.remove(temp_photo_path)

    # Generar la respuesta usando Gemini
    response = generate_response(caption, spad_prediction)
    
    message = (
        f"{user_first_name}, el contenido de clorofila de tu hoja en unidades SPAD ±3 es: {spad_prediction:.2f}.\n\n"
        f"{response}"
    )
    update.message.reply_text(message, parse_mode='Markdown')

def generate_response(caption, spad_prediction):
    question = (
        f"Actúa como expero en delitos de hurto"
        f"Actúa siempre con una postura de seguridad"
        f"La descripción del delito proporcionada por el usuario es la siguiente: {caption}."
        )    
    response = generate_agronomic_response(question)
    return response
