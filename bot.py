import requests
from telegram.ext import Updater, MessageHandler, Filters
from datetime import datetime
import re

FIREBASE_URL = "https://sinais-double-default-rtdb.firebaseio.com/"

mapa_cores = {
    "⚫️": "Preto",
    "🔴": "Vermelho",
    "🟢": "Verde",
    "⚪️": "Branco"
}

def enviar_para_firebase(sinal):
    hora_atual = datetime.now().strftime("%H:%M")
    dados = {
        "Horario": hora_atual,
        "Entre Agora na Cor": sinal["cor"],
        "Gales": sinal["gale"],
        "Jogo": "Double"
    }
    requests.post(FIREBASE_URL + "/sinais.json", json=dados)

def extrair_sinal(mensagem):
    match_cor = re.search(r"Entrada No:\s*(.*?)\s+e proteção", mensagem)
    match_gale = re.search(r"(SEM GALE|0 tentativa|1 tentativa|1 tentativa!)", mensagem)

    if not match_cor or not match_gale:
        return None

    cor_emoji = match_cor.group(1).strip()
    cor = mapa_cores.get(cor_emoji)

    if cor is None:
        return None

    gale = 0 if "SEM" in match_gale.group(1) or "0" in match_gale.group(1) else 1

    return {"cor": cor, "gale": gale}

def processar(update, context):
    mensagem = update.message.text
    sinal = extrair_sinal(mensagem)
    if sinal:
        enviar_para_firebase(sinal)

def main():
    updater = Updater("7772900897:AAGKUIL7U6EDZWth4Nqd2-RhvQGIBm0ud3Y", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, processar))
    updater.start_polling()
    print("🤖 Bot rodando e monitorando mensagens...")
    updater.idle()

if __name__ == "__main__":
    main()
