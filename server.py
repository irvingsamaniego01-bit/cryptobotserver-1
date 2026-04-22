from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8714363713:AAHkr1Uj4YDFQFpN2MZ_5XQVdSDEJGQoxa8")
CHAT_ID        = os.environ.get("CHAT_ID", "1589285187")

def send_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    tipo    = data.get("tipo", "").upper()
    ticker  = data.get("ticker", "???")
    precio  = data.get("precio", "???")
    rsi     = data.get("rsi", "???")
    razon   = data.get("razon", "Confluencia detectada")

    if tipo == "COMPRA":
        mensaje = (
            f"🟢 <b>SENAL DE COMPRA</b>\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📌 Par: <b>{ticker}</b>\n"
            f"💰 Precio: <b>${precio}</b>\n"
            f"📊 RSI: <b>{rsi}</b>\n"
            f"📐 Razon: {razon}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⚠️ Recuerda: Confirma siempre antes de operar"
        )
    elif tipo == "VENTA":
        mensaje = (
            f"🔴 <b>SENAL DE VENTA</b>\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📌 Par: <b>{ticker}</b>\n"
            f"💰 Precio: <b>${precio}</b>\n"
            f"📊 RSI: <b>{rsi}</b>\n"
            f"📐 Razon: {razon}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⚠️ Recuerda: Confirma siempre antes de operar"
        )
    else:
        mensaje = f"📩 Alerta recibida:\n{data}"

    send_telegram(mensaje)
    return jsonify({"status": "ok"}), 200

@app.route("/test", methods=["GET"])
def test():
    send_telegram(
        "✅ <b>Bot conectado correctamente</b>\n"
        "━━━━━━━━━━━━━━━\n"
        "🤖 CryptoBot Pro activo\n"
        "📡 Esperando senales de TradingView..."
    )
    return jsonify({"status": "mensaje enviado a Telegram"}), 200

@app.route("/", methods=["GET"])
def home():
    return "CryptoBot Pro - Servidor activo ✅", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
