from telegram.ext import ApplicationBuilder, MessageHandler, filters
from fastapi import FastAPI, Request
import os
import requests
import json

FIREBASE_URL = "https://sinais-double-default-rtdb.firebaseio.com/sinais.json"
TOKEN = "7772900897:AAGKUIL7U6EDZWth4Nqd2-RhvQGIBm0ud3Y"

app_telegram = ApplicationBuilder().token(TOKEN).build()
app = FastAPI()

# Função para enviar mensagem ao Firebase
def enviar_para_firebase(texto):
    linhas = texto.splitlines()
    dados = {}

    for linha in linhas:
        if "Entrada No" in linha:
            if "⚫️" in linha:
                dados["Entre Agora na Cor"] = "Preto"
            elif "🔴" in linha:
                dados["Entre Agora na Cor"] = "Vermelho"
            elif "🟢" in linha:
                dados["Entre Agora na Cor"] = "Verde"
            elif "⚪️" in linha:
                dados["Entre Agora na Cor"] = "Branco"
        elif "Horário" in linha or "⌚" in linha:
            hora = linha.split()[-1]
            dados["Horario"] = hora.strip()
        elif "Gale" in linha or "GALE" in linha:
            if "1" in linha:
                dados["Gales"] = 1
            elif "2" in linha:
                dados["Gales"] = 2
            else:
                dados["Gales"] = 0

    dados["Jogo"] = "Double"

    if "Entre Agora na Cor" in dados and "Horario" in dados:
        try:
            requests.post(FIREBASE_URL, json=dados)
            print("✅ Sinal enviado:", dados)
        except Exception as e:
            print("Erro ao enviar para Firebase:", e)

@app.post(f"/{TOKEN}")
async def webhook(req: Request):
    data = await req.json()
    await app_telegram.update_queue.put(data)
    return "ok"

async def handle(update, context):
    texto = update.message.text
    if texto:
        enviar_para_firebase(texto)

app_telegram.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle))

@app.on_event("startup")
async def startup():
    webhook_url = f"https://bot-telegram-firebase-production.up.railway.app/{TOKEN}"
    await app_telegram.bot.set_webhook(webhook_url)