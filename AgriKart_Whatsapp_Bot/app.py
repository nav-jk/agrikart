# app.py

import os
import json
import requests
from flask import Flask, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load credentials from environment variables
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')

# --- In-memory database for hackathon prototype ---
# This dictionary will store the state and data for each user (farmer)
user_states = {}

# --- This single function will handle both GET and POST requests ---
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # Handle the GET request (for webhook verification)
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode and token and mode == 'subscribe' and token == VERIFY_TOKEN:
            print('SUCCESS: Webhook verified')
            return challenge, 200
        else:
            print('ERROR: Verification tokens do not match')
            return 'Verification token mismatch', 403

    # Handle the POST request (for incoming messages from farmers)
    elif request.method == 'POST':
        data = request.get_json()
        print("--- INCOMING POST REQUEST (MESSAGE) ---")
        print(json.dumps(data, indent=2))
        print("---------------------------------------")

        try:
            # Ensure the incoming message is a valid WhatsApp message
            if (data.get('object') == 'whatsapp_business_account' and
                data['entry'][0]['changes'][0]['value'].get('messages')):

                message_data = data['entry'][0]['changes'][0]['value']['messages'][0]
                from_number = message_data['from']
                msg_body = message_data['text']['body']

                # --- AgriKart.ai Bot Logic ---

                # Check if this is a new farmer
                if from_number not in user_states:
                    user_states[from_number] = {'state': 'awaiting_name', 'data': {}}
                    reply_body = "Welcome to AgriKart.ai! We need to register you first.\n\nWhat is your full name?"
                    send_whatsapp_message(from_number, reply_body)
                    return 'OK', 200

                # Get the current state for this farmer
                current_state = user_states[from_number]['state']
                
                # State: Awaiting Farmer's Name
                if current_state == 'awaiting_name':
                    user_states[from_number]['data']['name'] = msg_body
                    user_states[from_number]['state'] = 'awaiting_village'
                    reply_body = f"Thank you, {msg_body}. What is your village name?"
                    send_whatsapp_message(from_number, reply_body)

                # State: Awaiting Farmer's Village
                elif current_state == 'awaiting_village':
                    user_states[from_number]['data']['village'] = msg_body
                    user_states[from_number]['state'] = 'awaiting_pincode'
                    reply_body = "Got it. And what is your 6-digit pincode?"
                    send_whatsapp_message(from_number, reply_body)
                
                # State: Awaiting Farmer's Pincode
                elif current_state == 'awaiting_pincode':
                    user_states[from_number]['data']['pincode'] = msg_body
                    user_states[from_number]['data']['produces'] = []
                    user_states[from_number]['state'] = 'awaiting_crop_name'
                    reply_body = "Registration complete! Let's list your produce.\n\nWhat is the name of the crop you would like to sell?"
                    send_whatsapp_message(from_number, reply_body)

                # State: Awaiting the name of the crop
                elif current_state == 'awaiting_crop_name':
                    user_states[from_number]['temp_produce'] = {'name': msg_body}
                    user_states[from_number]['state'] = 'awaiting_price'
                    reply_body = f"Okay, crop is '{msg_body}'. What is your suggested price per kg? (e.g., 25)"
                    send_whatsapp_message(from_number, reply_body)

                # State: Awaiting the price
                elif current_state == 'awaiting_price':
                    user_states[from_number]['temp_produce']['price_per_kg'] = msg_body
                    user_states[from_number]['state'] = 'awaiting_quantity'
                    reply_body = "And what is the total quantity (in kg) you have available?"
                    send_whatsapp_message(from_number, reply_body)

                # State: Awaiting the quantity
                elif current_state == 'awaiting_quantity':
                    user_states[from_number]['temp_produce']['quantity_kg'] = msg_body
                    user_states[from_number]['data']['produces'].append(user_states[from_number]['temp_produce'])
                    del user_states[from_number]['temp_produce']
                    user_states[from_number]['state'] = 'awaiting_more_crops'
                    reply_body = "Your produce has been noted. Would you like to add another crop? (Please type Yes or No)"
                    send_whatsapp_message(from_number, reply_body)

                # State: Awaiting if they want to add more crops
                elif current_state == 'awaiting_more_crops':
                    if 'yes' in msg_body.lower():
                        user_states[from_number]['state'] = 'awaiting_crop_name'
                        reply_body = "Great! What is the name of the next crop?"
                        send_whatsapp_message(from_number, reply_body)
                    else:
                        print("--- FINAL DATA FOR FARMER ---")
                        print(json.dumps(user_states[from_number]['data'], indent=2))
                        print("-----------------------------")
                        
                        reply_body = "Thank you! All your produce has been listed. We will notify you when we get orders for your items."
                        send_whatsapp_message(from_number, reply_body)
                        user_states[from_number]['state'] = 'conversation_over'

                # State: Conversation is over, wait for a new greeting to start again
                elif current_state == 'conversation_over':
                    command = msg_body.lower()
                    if 'hi' in command or 'hello' in command:
                        user_states[from_number]['state'] = 'awaiting_crop_name'
                        reply_body = "Welcome back! What is the name of the crop you would like to sell today?"
                        send_whatsapp_message(from_number, reply_body)
                    else:
                        reply_body = "You're welcome! Feel free to message 'hi' anytime you want to list more produce."
                        send_whatsapp_message(from_number, reply_body)

        except Exception as e:
            print(f"Error processing message: {e}")
            pass

        return 'OK', 200
    else:
        return 'Method Not Allowed', 405


def send_whatsapp_message(to_number, message_text):
    """Sends a text message to a WhatsApp number."""
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Message sent to {to_number}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")


if __name__ == '__main__':
    app.run(port=5000, debug=True)