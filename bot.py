
import os
import requests
from telegram.ext import Updater, MessageHandler, Filters
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

FIREBASE_URL = os.getenv("FIREBASE_URL")
TOKEN = os.getenv("TOKEN")

mapa_cores = {
    "⚫️": "Preto",
    "🔴": "Vermelho",
    "🟢": "Verde",
    "⚪️": "Branco"
}

def extrair_sinal(mensagem):
    linhas = mensagem.splitlines()
    cor = None
    gales = 0

    for linha in linhas:
        if "Entrada" in linha and "⚫️" in linha:
            cor = mapa_cores.get("⚫️")
        elif "Entrada" in linha and "🔴" in linha:
            cor = mapa_cores.get("🔴")
        elif "Entrada" in linha and "🟢" in linha:
            cor = mapa_cores.get("🟢")
        elif "Entrada" in linha and "⚪️" in linha:
            cor = mapa_cores.get("⚪️")
        if "SEM GALE" in linha:
            gales = 0
        elif "1 tentativa" in linha or "1 Gale" in linha:
            gales = 1
        elif "2 Gale" in linha or "2 tentativas" in linha:
            gales = 2

    if cor:
        return {
            "Horario": datetime.now().strftime("%H:%M"),
            "Entre Agora na Cor": cor,
            "Gales": gales,
            "Jogo": "Double"
        }
    return None

def enviar_para_firebase(dados):
    try:
        response = requests.post(FIREBASE_URL, json=dados)
        print("Enviado:", response.status_code, response.text)
    except Exception as e:
        print("Erro ao enviar:", e)

def processar_mensagem(update, context):
    texto = update.message.text
    if texto:
        sinal = extrair_sinal(texto)
        if sinal:
            enviar_para_firebase(sinal)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, processar_mensagem))
    updater.start_polling()
    print("🤖 Bot rodando e monitorando mensagens...")
    updater.idle()

if __name__ == "__main__":
    main()
