import os
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

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
def get_farmer_produce(access_token):
    """Fetch all produce for the logged-in farmer"""
    url = f"{API_BASE_URL}/api/v1/produce/"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to fetch produce. Status: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error fetching produce list: {e}")
        return []


def check_farmer_exists(phone_number):
    url = f"{API_BASE_URL}/api/v1/farmer/check/{phone_number}/"
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

# --- Webhook ---
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if (request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFY_TOKEN):
            return request.args.get('hub.challenge'), 200
        return 'Unauthorized', 403

    data = request.get_json()
    try:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        from_number = message['from']
        msg_body = message['text']['body']
        command = msg_body.lower()

                # 💼 Dashboard Command
        if command in ['dashboard', 'my produce']:
            access_token = user_states[from_number].get('access_token')
            if not access_token:
                send_whatsapp_message(from_number, "⚠️ You're not logged in. Please type 'hi' to start.")
                return 'OK', 200

            produce_list = get_farmer_produce(access_token)
            if not produce_list:
                send_whatsapp_message(from_number, "🧺 You have no produce listed yet.")
                return 'OK', 200

            lines = ["📊 *Your Produce Dashboard:*"]
            for p in produce_list:
                status = "✅" if p.get("is_active", True) else "❌"
                lines.append(
                    f"• {p['name']} - ₹{p['price']}/kg - {p['quantity']}kg {status}"
                )

            send_whatsapp_message(from_number, "\n".join(lines))
            return 'OK', 200

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
            user_states[from_number]['temp_produce'] = {'name': msg_body}
            user_states[from_number]['state'] = 'awaiting_price'
            send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['ask_price'])

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

        if not phone or not items:
            return jsonify({"error": "Invalid data"}), 400

        message_lines = ["🧾 *Order Update:*"]
        for item in items:
            message_lines.append(
                f"📦 {item['produce']}: bought {item['quantity_bought']}kg\n"
                f"📊 Remaining stock: {item['remaining_stock']}kg"
            )
        message = "\n\n".join(message_lines)
        send_whatsapp_message(phone, message)

        return jsonify({"status": "sent"}), 200
    except Exception as e:
        print(f"❌ Error in /notify-farmer: {e}")
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    print("🚀 WhatsApp Bot Running...")
    app.run(port=5000, debug=True)