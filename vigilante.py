import os
import requests
import psycopg2
import time
from datetime import datetime

#   Configuración
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "db_crypto")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "ERROR_NO_PASSWORD")

#   Configuración de telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "ERROR_NO_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "ERROR_NO_ID")


#   Funciones
def obtener_precio_bitcoin():
    # Consultar API publica de CoinGeko
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        respuesta = requests.get(url)
        datos = respuesta.json()
        precio = datos["bitcoin"]["usd"]
        return precio
    except Exception as e:
        print(f"Error obteniendo precio: {e}")
        return None


def guardar_en_db(precio):
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO precios_btc (precio_usd) VALUES (%s)", (precio,))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Precio ${precio} guardado en DB.")
    except Exception as e:
        print(f"Error guardando en DB: {e}")


def enviar_alerta_telegram(mensaje):
    #   Envia mensaje al telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    requests.post(url, json=payload)


#    Lógica Principal
def main():
    print("--- INICIANDO VIGILANCIA ---")

    # 1.    Extract (Sacar precio)
    precio_actual = obtener_precio_bitcoin()

    if precio_actual:
        # 2.    Load
        guardar_en_db(precio_actual)

        # 3.    Alert
        mensaje = f"💰 Bitcoin Actual: ${precio_actual} USD"
    # enviar_alerta_telegram(mensaje)
    # print("Alerta enviada a Telegram.")
    else:
        print(f"No se pudo obtener el precio.")


if __name__ == "__main__":
    print("🤖 BOT INICIADO - Presiona Ctrl+C para detener")

    while True:  # <--- BUCLE INFINITO
        try:
            main()  # Ejecuta la lógica
        except Exception as e:
            print(f"❌ Error crítico en el loop: {e}")

        # Esperar 60 segundos antes de la próxima revisión
        print("⏳ Esperando 1 minuto...")
        time.sleep(60)
