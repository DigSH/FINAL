import google.generativeai as genai
import joblib
import mercadopago
from config.config import GOOGLE_API_KEY, MERCADO_PAGO_ACCESS_TOKEN

class DependencyInjector:
    def __init__(self):
        # Configurar Mercado Pago
        self.mercado_pago_sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)
        
        # Cargar el modelo y el escalador
        self.model = joblib.load('models/model.pkl')
        self.scaler = joblib.load('models/scaler.pkl')
        
        # Configurar Google Generative AI
        genai.configure(api_key=GOOGLE_API_KEY)
        self.gemini_model = genai.GenerativeModel('gemini-pro')

injector = DependencyInjector()