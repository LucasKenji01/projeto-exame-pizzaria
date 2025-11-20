import os
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pizzaria.db")
SECRET_KEY = os.getenv("SECRET_KEY", "ALTERE_ESTA_CHAVE_EM_PRODUCAO")
TOKEN_EXPIRATION_MINUTES = int(os.getenv("TOKEN_EXPIRATION_MINUTES", "120"))
