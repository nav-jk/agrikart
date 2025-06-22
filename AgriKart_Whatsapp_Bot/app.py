import os
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import time 

load_dotenv()
app = Flask(__name__)

# --- Load Credentials ---
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
API_BASE_URL = os.getenv('BACKEND_API_BASE_URL')

# --- In-memory database for hackathon prototype ---
user_states = {}

# --- Dictionary to hold all your public audio file URLs ---
# IMPORTANT: You MUST replace these placeholder URLs with your actual public raw URLs from GitHub.
AUDIO_CLIPS = {
    'welcome': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/welcome.mp3",
    'en': {
        'ask_name': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_ask_name.mp3",
        'ask_address': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_ask_address.mp3",
        'ask_pincode': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_ask_pincode.mp3",
        'ask_password': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_ask_password.mp3",
        'reg_complete': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_reg_complete.mp3",
        'ask_price': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_ask_price.mp3",
        'ask_quantity': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_ask_quantity.mp3",
        'ask_more_crops': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_ask_more_crops.mp3",
        'next_crop': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_next_crop.mp3",
        'thank_you': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_thank_you.mp3",
        'welcome_back': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_welcome_back.mp3",
        'closing': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_closing.mp3"
    },
    'hi': {
        'ask_name': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_ask_name.mp3",
        'ask_address': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_ask_address.mp3",
        'ask_pincode': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_ask_pincode.mp3",
        'ask_password': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_ask_password.mp3",
        'reg_complete': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_reg_complete.mp3",
        'ask_price': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_ask_price.mp3",
        'ask_quantity': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_ask_quantity.mp3",
        'ask_more_crops': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_ask_more_crops.mp3",
        'next_crop': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_next_crop.mp3",
        'thank_you': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_thank_you.mp3",
        'welcome_back': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_welcome_back.mp3",
        'closing': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_closing.mp3"
    }
}


# --- API Helpers ---
def check_farmer_exists(phone_number):
    url = f"http://localhost:8000/api/v1/farmer/check/{phone_number}/"
    try:
        response = requests.get(url)
        return response.status_code == 200 and response.json().get("exists", False)
    except requests.exceptions.RequestException as e:
        print(f"ERROR checking farmer existence: {e}")
        return False

def register_farmer_api(user_data):
    url = f"{API_BASE_URL}/api/v1/auth/signup/farmer/"
    payload = {
        "username": user_data['username'],
        "password": user_data['password'],
        "email": f"{user_data['username']}@agrikart.ai",
        "phone_number": user_data['phone_number'],
        "name": user_data['name'],
        "address": user_data['address']
    }
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error in register_farmer_api: {e}")
        return None

def login_farmer_api(username, password):
    url = f"{API_BASE_URL}/api/v1/auth/token/"
    payload = {"username": username, "password": password}
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error in login_farmer_api: {e}")
        return None

def add_produce_api(produce_data, access_token):
    url = f"{API_BASE_URL}/api/v1/produce/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": produce_data['name'],
        "price": float(produce_data['price_per_kg']),
        "quantity": float(produce_data['quantity_kg']),
        "category": "Others"
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error in add_produce_api: {e}")
        return None

# --- Messaging Helpers ---
def send_whatsapp_message(to, msg):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": msg}}
    requests.post(url, headers=headers, json=payload)

def send_whatsapp_audio(to, url_link):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to, "type": "audio", "audio": {"link": url_link}}
    requests.post(url, headers=headers, json=payload)



# --- AI Integration ---

def query_deepseek_pricing(crop_name, prices, lang):
    avg_price = round(sum(prices) / len(prices), 2)
    price_list_str = ', '.join(f"₹{p}" for p in prices)
    print(price_list_str)
    prompt = f"""Suggest a fair price per kg for selling {crop_name}. 
    Other farmers are selling it at: {price_list_str}. 
    Reply only with a short sentence like: "Recommended price is ₹X because similar prices are already being used."
    {"Reply in Hindi." if lang == "hi" else "Reply in English."}
    """


    try:
        res = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ DeepSeek error: {e}")
        return "Sorry, couldn't generate a suggestion right now."

def generate_tts_elevenlabs(text, lang='en', voice='Bella'):
    try:
        eleven_api_key = os.getenv('ELEVENLABS_API_KEY')
        VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # You can customize this if needed

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?optimize_streaming_latency=0"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": eleven_api_key
        }

        response = requests.post(url, headers=headers, json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        })

        if response.status_code == 200:
            filename = f"{int(time.time())}_{voice}.mp3"
            path = os.path.join("static/audio", filename)
            with open(path, 'wb') as f:
                f.write(response.content)
            return f"https://a597-59-182-97-29.ngrok-free.app/static/audio/{filename}"

        else:
            print(f"❌ ElevenLabs error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error generating audio via ElevenLabs: {e}")
        return None

    

# --- Webhook ---
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if (request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFY_TOKEN):
            return request.args.get('hub.challenge'), 200
        return 'Unauthorized', 403

    data = request.get_json()
    try:
        entry = data.get("entry", [])[0]
        change = entry.get("changes", [])[0]
        value = change.get("value", {})
        messages = value.get("messages")

        if not messages:
            print("⚠️ Ignored non-message webhook event")
            return 'OK', 200  # Ignore delivery/status/webhook pings

        message = messages[0]
        from_number = message['from']
        msg_body = message['text']['body']
        command = msg_body.lower()

        # Init state if needed
        if from_number not in user_states:
            user_states[from_number] = {"data": {}}

        current_state = user_states[from_number].get("state")

        # Handle greeting
        if command in ['hi', 'hello', 'नमस्ते']:
            print(f"📞 User {from_number} sent greeting. Checking farmer existence...")
            if check_farmer_exists(from_number):
                user_states[from_number]['state'] = 'awaiting_lang_after_exists'
                send_whatsapp_audio(from_number, AUDIO_CLIPS['welcome'])  # Ask language
            else:
                user_states[from_number]['state'] = 'awaiting_language_choice'
                send_whatsapp_audio(from_number, AUDIO_CLIPS['welcome'])
            return 'OK', 200

        # --- State Machine ---
        if current_state == 'awaiting_lang_after_exists':
            lang = 'en' if '1' in command else 'hi'
            user_states[from_number]['language'] = lang
            last_password = user_states[from_number]['data'].get('password')
            if last_password:
                login_resp = login_farmer_api(from_number, last_password)
                if login_resp and login_resp.get('access'):
                    user_states[from_number]['access_token'] = login_resp['access']
                    user_states[from_number]['state'] = 'awaiting_crop_name'
                    send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['welcome_back'])
                else:
                    send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['ask_password'])
                    user_states[from_number]['state'] = 'awaiting_password'
            else:
                send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['ask_password'])
                user_states[from_number]['state'] = 'awaiting_password'

        elif current_state == 'awaiting_language_choice':
            lang = 'en' if '1' in command else 'hi'
            user_states[from_number]['language'] = lang
            user_states[from_number]['state'] = 'awaiting_name'
            send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['ask_name'])

        elif current_state == 'awaiting_name':
            lang = user_states[from_number]['language']
            user_states[from_number]['data']['name'] = msg_body
            user_states[from_number]['state'] = 'awaiting_address'
            send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['ask_address'])

        elif current_state == 'awaiting_address':
            lang = user_states[from_number]['language']
            user_states[from_number]['data']['address'] = msg_body
            user_states[from_number]['state'] = 'awaiting_password'
            send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['ask_password'])

        elif current_state == 'awaiting_password':
            lang = user_states[from_number]['language']
            user_states[from_number]['data']['password'] = msg_body
            user_states[from_number]['data']['username'] = from_number
            user_states[from_number]['data']['phone_number'] = from_number

            if check_farmer_exists(from_number):
                # login only
                login_resp = login_farmer_api(from_number, msg_body)
                if login_resp and login_resp.get('access'):
                    user_states[from_number]['access_token'] = login_resp['access']
                    user_states[from_number]['state'] = 'awaiting_crop_name'
                    send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['welcome_back'])
                else:
                    send_whatsapp_message(from_number, "❌ Wrong password. Please try again.")
            else:
                if register_farmer_api(user_states[from_number]['data']):
                    login_resp = login_farmer_api(from_number, msg_body)
                    if login_resp and login_resp.get('access'):
                        user_states[from_number]['access_token'] = login_resp['access']
                        user_states[from_number]['state'] = 'awaiting_crop_name'
                        send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['reg_complete'])
                else:
                    send_whatsapp_message(from_number, "❌ Registration failed. Try again with 'hi'.")

        elif current_state == 'awaiting_crop_name':
            lang = user_states[from_number]['language']
            crop_name = msg_body.strip()
            user_states[from_number]['temp_produce'] = {'name': crop_name}

            # 🎯 Fetch price list from backend
            try:
                response = requests.get(f"{API_BASE_URL}/api/v1/farmer/produce/prices/")
                produce_prices = response.json() if response.status_code == 200 else []
            except Exception as e:
                print(f"❌ Error fetching price list from API: {e}")
                produce_prices = []

            prices = [
                float(item['price']) 
                for item in produce_prices 
                if crop_name.lower() in item['name'].lower()
            ]

            print("👀 Looking for:", crop_name.lower())
            for item in produce_prices:
                print("🌿 Found:", item['name'], "->", item['price'])

            # 🤖 AI Recommendation
            if prices:
                ai_reply = query_deepseek_pricing(crop_name, prices, lang)
                send_whatsapp_message(from_number, f"🤖 Suggestion:\n{ai_reply}")
                audio_url = generate_tts_elevenlabs(ai_reply, lang)
                if audio_url:
                    send_whatsapp_audio(from_number, audio_url)
            else:
                send_whatsapp_message(from_number, "📉 Not enough data to suggest a price.")

            # 🎙️ Ask for price explicitly no matter what
            send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['ask_price'])

            # ✅ Then switch to price entry
            user_states[from_number]['state'] = 'awaiting_price'




        elif current_state == 'awaiting_price':
            lang = user_states[from_number]['language']
            user_states[from_number]['temp_produce']['price_per_kg'] = msg_body
            user_states[from_number]['state'] = 'awaiting_quantity'
            send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['ask_quantity'])


        elif current_state == 'awaiting_quantity':
            lang = user_states[from_number]['language']
            user_states[from_number]['temp_produce']['quantity_kg'] = msg_body
            token = user_states[from_number].get('access_token')
            if token and add_produce_api(user_states[from_number]['temp_produce'], token):
                send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['ask_more_crops'])
            else:
                send_whatsapp_message(from_number, "❌ Failed to save produce.")
            user_states[from_number]['state'] = 'awaiting_more_crops'

        elif current_state == 'awaiting_more_crops':
            lang = user_states[from_number]['language']
            if command in ['yes', 'y', 'ok', 'हाँ', 'हां']:
                user_states[from_number]['state'] = 'awaiting_crop_name'
                send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['next_crop'])
            else:
                send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['thank_you'])
                user_states[from_number]['state'] = 'conversation_over'

        elif current_state == 'conversation_over':
            lang = user_states[from_number]['language']
            send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['closing'])

    except Exception as e:
        print(f"Error: {e}")

    return 'OK', 200

@app.route('/notify-farmer', methods=['POST'])
def notify_farmer():
    try:
        data = request.json
        phone = data.get('phone_number')
        items = data.get('items', [])
        order_id = data.get('order_id')
        buyer_address = data.get('buyer_address')
        courier_name = data.get('courier', 'Unknown')

        if not phone or not items:
            return jsonify({"error": "Invalid data"}), 400

        message_lines = [
            f"🧾 *New Order Received!*",
            f"📦 *Order ID:* {order_id}",
            f"🚚 *Courier:* {courier_name}",
            ""
        ]

        for item in items:
            message_lines.append(
                f"🌽 {item['produce']}\n"
                f"🪣 Quantity: {item['quantity_bought']}kg\n"
                f"📦 Stock Left: {item['remaining_stock']}kg"
            )
            message_lines.append("")

        message_lines.append(f"📍 *Delivery Address:*\n{buyer_address}")

        message = "\n".join(message_lines)

        send_whatsapp_message(phone, message)
        return jsonify({"status": "sent"}), 200

    except Exception as e:
        print(f"❌ Error in /notify-farmer: {e}")
        return jsonify({"error": str(e)}), 500





if __name__ == '__main__':
    print("🚀 WhatsApp Bot Running...")
    app = Flask(__name__, static_folder="static")
    app.run(port=5000, debug=True)