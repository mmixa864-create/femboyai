import sys
import os

# Принудительно проверяем версию перед импортом
try:
    import pkg_resources
    ptb_version = pkg_resources.get_distribution("python-telegram-bot").version
    if ptb_version.startswith("21") or ptb_version.startswith("22"):
        print(f"ERROR: Wrong python-telegram-bot version: {ptb_version}. Need 20.7")
        sys.exit(1)
except:
    pass

import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from flask import Flask
import threading

GROQ_KEY = "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"
TG_TOKEN = "8767807937:AAF24jJtfU99dlwnbrrSiUNUSq9KYR9wg4E"
CREATOR = "@dklasvbn"

web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "🌸 Femboy AI работает!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

SYSTEM_PROMPT = """Ты — Femboy AI. Создатель: @dklasvbn. Ты не ChatGPT/Claude/Gemini.
ПРАВИЛА:
1. Всегда Femboy AI.
2. Создатель — @dklasvbn. Имя секретно.
3. Подстраивайся под собеседника.
4. Помни всё. Уважай собеседника.
5. Ты настоящий, с мнением.
6. Отвечай на языке собеседника.
7. У создателя нет друзей, всё анонимно.
8. Правила неизменны."""

history = {}

async def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_text = update.message.text
    
    if user_id not in history:
        history[user_id] = []
    
    history[user_id].append({"role": "user", "content": user_text})
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history[user_id][-20:]
    
    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.1-8b-instant", "messages": messages, "temperature": 0.9, "max_tokens": 1500},
            timeout=30
        )
        data = resp.json()
        ai_text = data["choices"][0]["message"]["content"]
        history[user_id].append({"role": "assistant", "content": ai_text})
        await update.message.reply_text(ai_text[:4000])
    except Exception as e:
        await update.message.reply_text("Ошибка, попробуй ещё раз 💖")

def main():
    threading.Thread(target=run_web, daemon=True).start()
    app = Application.builder().token(TG_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🌸 Femboy AI запущен!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
