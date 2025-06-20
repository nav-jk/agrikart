import os
import json
import requests
from flask import Flask, request
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


# --- API Helper Functions ---
def register_farmer_api(user_data):
    """Calls the backend API to register a new farmer."""
    url = f"{API_BASE_URL}/api/v1/auth/signup/farmer/"
    payload = {
        "username": user_data.get('username'),
        "password": user_data.get('password'),
        "email": f"{user_data.get('username')}@agrikart.ai", # Auto-generates dummy email
        "phone_number": user_data.get('phone_number'),
        "name": user_data.get('name'),
        "address": user_data.get('address') # This now includes village
    }
    print(f"--- Attempting to register farmer: POST {url} ---")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("--- Farmer registration successful ---")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"--- ERROR in farmer registration API: {e.response.text if e.response else e} ---")
        return None

def login_farmer_api(username, password):
    """Calls the backend API to log in and get JWT tokens."""
    url = f"{API_BASE_URL}/api/v1/auth/token/"
    payload = {"username": username, "password": password}
    print(f"--- Attempting to login farmer: POST {url} ---")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("--- Farmer login successful ---")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"--- ERROR in farmer login API: {e.response.text if e.response else e} ---")
        return None

def add_produce_api(produce_data, access_token):
    """Calls the backend API to add a new produce item."""
    url = f"{API_BASE_URL}/api/v1/produce/"
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {
        "name": produce_data.get('name'),
        "price_per_kg": float(produce_data.get('price_per_kg', 0)),
        "quantity_kg": float(produce_data.get('quantity_kg', 0))
    }
    print(f"--- Attempting to add produce: POST {url} ---")
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print("--- Add produce successful ---")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"--- ERROR in add produce API: {e.response.text if e.response else e} ---")
        return None

# --- Messaging Functions ---
def send_whatsapp_message(to_number, message_text):
    """Sends a text message to a WhatsApp number."""
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}','Content-Type': 'application/json'}
    payload = {"messaging_product": "whatsapp","to": to_number,"type": "text","text": {"body": message_text}}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending text message: {e}")

def send_whatsapp_audio(to_number, audio_url):
    """Sends an audio message from a public URL."""
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}','Content-Type': 'application/json'}
    payload = {"messaging_product": "whatsapp","to": to_number,"type": "audio","audio": {"link": audio_url}}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Audio message sent to {to_number}.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending audio message: {e}")

# --- Main Webhook Logic ---
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode and token and mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'Verification token mismatch', 403

    elif request.method == 'POST':
        data = request.get_json()
        print(f"--- INCOMING POST REQUEST ---\n{json.dumps(data, indent=2)}\n---------------------------")

        try:
            if data['entry'][0]['changes'][0]['value'].get('messages'):
                message_data = data['entry'][0]['changes'][0]['value']['messages'][0]
                from_number = message_data['from']
                msg_body = message_data['text']['body']
                command = msg_body.lower()

                # Always start with language choice on a greeting
                if 'hi' in command or 'hello' in command or 'नमस्ते' in command:
                    user_states[from_number] = user_states.get(from_number, {'data': {}})
                    user_states[from_number]['state'] = 'awaiting_language_choice'
                    send_whatsapp_audio(from_number, AUDIO_CLIPS['welcome'])
                    return 'OK', 200

                current_state = user_states.get(from_number, {}).get('state')

                if not current_state:
                    send_whatsapp_audio(from_number, AUDIO_CLIPS['welcome'])
                    return 'OK', 200

                # --- State Machine ---
                
                if current_state == 'awaiting_language_choice':
                    lang = 'en'
                    if '2' in command:
                        lang = 'hi'
                    user_states[from_number]['language'] = lang
                    
                    if user_states[from_number].get('data', {}).get('pincode'):
                        user_states[from_number]['state'] = 'awaiting_crop_name'
                        send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['welcome_back'])
                    else:
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

                    if register_farmer_api(user_states[from_number]['data']):
                        login_response = login_farmer_api(from_number, msg_body)
                        if login_response and login_response.get('access'):
                            user_states[from_number]['access_token'] = login_response['access']
                            user_states[from_number]['state'] = 'awaiting_crop_name'
                            send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['reg_complete'])
                        else:
                            send_whatsapp_message(from_number, "Registration was successful, but we couldn't log you in. Please message 'hi' to try again.")
                    else:
                        send_whatsapp_message(from_number, "Sorry, registration failed. This phone number might already be registered. Please message 'hi' to start over.")

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
                    access_token = user_states[from_number].get('access_token')
                    
                    if access_token and add_produce_api(user_states[from_number]['temp_produce'], access_token):
                        send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['ask_more_crops'])
                    else:
                        send_whatsapp_message(from_number, "Sorry, there was an error saving your produce. Your session might have expired. Please message 'hi' to start again.")

                    del user_states[from_number]['temp_produce']
                    user_states[from_number]['state'] = 'awaiting_more_crops'

                elif current_state == 'awaiting_more_crops':
                    lang = user_states[from_number]['language']
                    yes_words = ['yes', 'yeah', 'yep', 'ok', 'हाँ', 'हा', 'han', 'ha']
                    
                    if any(word in command for word in yes_words):
                        user_states[from_number]['state'] = 'awaiting_crop_name'
                        send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['next_crop'])
                    else:
                        send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['thank_you'])
                        user_states[from_number]['state'] = 'conversation_over'
                
                elif current_state == 'conversation_over':
                    lang = user_states[from_number].get('language', 'en')
                    send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['closing'])

        except Exception as e:
            print(f"Error processing message: {e}")

        return 'OK', 200
    return 'Method Not Allowed', 405

if __name__ == '__main__':
    app.run(port=5000, debug=True)
