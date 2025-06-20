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

# --- In-memory database for hackathon prototype ---
user_states = {}

# --- Dictionary to hold all our audio file URLs ---
# IMPORTANT: You MUST replace these placeholder URLs with your actual public URLs.
AUDIO_CLIPS = {
    'welcome': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/welcome.mp3",
    'en': { 'ask_name': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_ask_name.mp3", 'ask_address': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_ask_address.mp3", 'ask_pincode': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_ask_pincode.mp3", 'reg_complete': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_reg_complete.mp3", 'ask_price': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_ask_price.mp3", 'ask_quantity': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_ask_quantity.mp3", 'ask_more_crops': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_ask_more_crops.mp3", 'next_crop': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_next_crop.mp3", 'thank_you': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_thank_you.mp3", 'welcome_back': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_welcome_back.mp3", 'closing': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/en_closing.mp3" },
    'hi': { 'ask_name': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_ask_name.mp3", 'ask_address': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_ask_address.mp3", 'ask_pincode': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_ask_pincode.mp3", 'reg_complete': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_reg_complete.mp3", 'ask_price': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_ask_price.mp3", 'ask_quantity': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_ask_quantity.mp3", 'ask_more_crops': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_ask_more_crops.mp3", 'next_crop': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_next_crop.mp3", 'thank_you': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_thank_you.mp3", 'welcome_back': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_welcome_back.mp3", 'closing': "https://raw.github.com/debdip4/agrikartwhatsappbot/main/Audio_files/hi_closing.mp3" }
}

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Webhook verification logic
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode and token and mode == 'subscribe' and token == VERIFY_TOKEN:
            print('SUCCESS: Webhook verified')
            return challenge, 200
        else:
            print('ERROR: Verification tokens do not match')
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

                # --- AgriKart.ai Voice Bot Logic ---
                
                if 'hi' in command or 'hello' in command or 'नमस्ते' in command:
                    user_states[from_number] = user_states.get(from_number, {'data': {}}) # Preserve data if user exists
                    user_states[from_number]['state'] = 'awaiting_language_choice'
                    send_whatsapp_audio(from_number, AUDIO_CLIPS['welcome'])
                    return 'OK', 200

                current_state = user_states.get(from_number, {}).get('state')

                if not current_state:
                    send_whatsapp_audio(from_number, AUDIO_CLIPS['welcome'])
                    return 'OK', 200

                # --- State Machine ---
                
                if current_state == 'awaiting_language_choice':
                    lang_choice = 'en'
                    if '2' in command:
                        lang_choice = 'hi'
                    
                    user_states[from_number]['language'] = lang_choice
                    
                    if user_states[from_number].get('data', {}).get('pincode'):
                        user_states[from_number]['state'] = 'awaiting_crop_name'
                        send_whatsapp_audio(from_number, AUDIO_CLIPS[lang_choice]['welcome_back'])
                    else:
                        # For registration, changing the question to be more generic
                        user_states[from_number]['state'] = 'awaiting_name'
                        send_whatsapp_audio(from_number, AUDIO_CLIPS[lang_choice]['ask_name'])

                elif current_state == 'awaiting_name':
                    lang = user_states[from_number]['language']
                    user_states[from_number]['data']['name'] = msg_body
                    user_states[from_number]['state'] = 'awaiting_address'
                    send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['ask_address'])

                elif current_state == 'awaiting_address':
                    lang = user_states[from_number]['language']
                    user_states[from_number]['data']['address'] = msg_body
                    user_states[from_number]['state'] = 'awaiting_pincode'
                    send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['ask_pincode'])
                
                elif current_state == 'awaiting_pincode':
                    lang = user_states[from_number]['language']
                    user_states[from_number]['data']['pincode'] = msg_body
                    user_states[from_number]['data']['produces'] = []
                    user_states[from_number]['state'] = 'awaiting_crop_name'
                    send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['reg_complete'])

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
                    user_states[from_number]['data']['produces'].append(user_states[from_number]['temp_produce'])
                    del user_states[from_number]['temp_produce']
                    user_states[from_number]['state'] = 'awaiting_more_crops'
                    send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['ask_more_crops'])

                elif current_state == 'awaiting_more_crops':
                    lang = user_states[from_number]['language']
                    
                    # --- THIS IS THE FIXED LOGIC ---
                    # List of words that mean "yes" in English, Hindi, and transliteration
                    yes_words = ['yes', 'yeah', 'yep', 'ok', 'हाँ', 'हा', 'han', 'ha','haan']
                    
                    # Check if any of the "yes" words are in the user's reply
                    if any(word in command for word in yes_words):
                        user_states[from_number]['state'] = 'awaiting_crop_name'
                        send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['next_crop'])
                    else:
                        # If the reply is "No", "ना", or anything else, end the conversation
                        print(f"--- FINAL DATA FOR FARMER ---\n{json.dumps(user_states[from_number]['data'], indent=2)}\n-----------------------------")
                        save_data_to_sheet(user_states[from_number]['data'])
                        send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['thank_you'])
                        user_states[from_number]['state'] = 'conversation_over'
                
                elif current_state == 'conversation_over':
                    lang = user_states[from_number].get('language', 'en')
                    send_whatsapp_audio(from_number, AUDIO_CLIPS[lang]['closing'])


        except Exception as e:
            print(f"Error processing message: {e}")

        return 'OK', 200
    return 'Method Not Allowed', 405

# The functions below this line (save_data_to_sheet, send_whatsapp_message, send_whatsapp_audio, etc.)
# remain exactly the same. They do not need to be changed.

def save_data_to_sheet(farmer_data):
    # This function is from our previous discussion and is assumed to be here.
    # It is not included again for brevity, but it should remain in your code.
    pass

def send_whatsapp_message(to_number, message_text):
    """Sends a text message to a WhatsApp number."""
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}','Content-Type': 'application/json'}
    payload = {"messaging_product": "whatsapp","to": to_number,"type": "text","text": {"body": message_text}}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Message sent to {to_number}. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

def send_whatsapp_audio(to_number, audio_url):
    """Sends an audio message from a public URL."""
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}','Content-Type': 'application/json'}
    payload = {"messaging_product": "whatsapp","to": to_number,"type": "audio","audio": {"link": audio_url}}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Audio message sent to {to_number}. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending audio message: {e}")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
