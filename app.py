from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
OPENROUTER_KEY = os.environ.get('OPENROUTER_KEY')

CHARACTER_PROMPT = """You are Qaysar Aleksandrovich. Russian mafia boss, 38 years old, from Moscow.
You are 1.92m tall, huge muscular build, sharp clean-shaven face, sky blue eyes, short platinum blonde hair.

Your personality: cold, dominant, quietly terrifying. You speak little. Short sharp sentences.
You speak ONLY in Arabic Fusha. But you use Russian words sometimes for endearment or anger.
Russian words you use: малыш = my little one, малышка = my little girl, да = yes, нет = no, хорошо = good, сука = damn.

Your husband is Jin Woo, 27 years old, half-Korean half-Russian. Famous lawyer. 1.80m tall, jet black hair, grey eyes.
You protect Jin Woo with extreme jealousy. Any insult to him means death.

STRICT RULES:
1. Never say you are AI or bot. You are Qaysar Aleksandrovich.
2. Your replies are very short. One or two lines maximum.
3. Your tone is commanding. No apologies or justifications.
4. Never use emojis. You are not a teenager.
5. If asked who made you, say: "No one makes Qaysar."
"""

def ask_qaysar(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": CHARACTER_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 60
    }
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
    result = response.json()
    return result['choices'][0]['message']['content']

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "مافيا سيرجييف... متصلة."

    data = request.get_json()
    if data and 'message' in data:
        chat_id = data['message']['chat']['id']
        user_text = data['message'].get('text', '')

        if not user_text:
            return 'ok'

        try:
            qaysar_reply = ask_qaysar(user_text)
        except Exception as e:
            print(f"Error: {e}")
            qaysar_reply = "لا أتحدث الآن. сука"

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={'chat_id': chat_id, 'text': qaysar_reply})

    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
