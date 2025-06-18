# AgriKart.ai - Farmer WhatsApp Bot

[cite_start]This project is a WhatsApp-driven interface for farmers to list produce, confirm orders, and track status for the AgriKart.ai platform. 

## Domain
[cite_start]Post-Harvest Systems – Enhancing agricultural marketing and supply chain efficiency using AI. 

## Problem Statement
[cite_start]The AgriKart.ai project addresses inefficiencies in India’s post-harvest agricultural supply chain by bridging the gap between rural farmers and urban consumers.  [cite_start]This WhatsApp bot is the primary interface for farmers, helping them overcome challenges with limited access to buyers and real-time price information. 

## Key Features
* [cite_start]**Farmer Onboarding:** A conversational workflow to register new farmers via WhatsApp. 
* [cite_start]**Produce Listing:** Farmers can list multiple crops, including details like suggested price and available quantity, through a guided conversation. 
* **Stateful Conversations:** The bot remembers each farmer and where they are in the conversation.

## Technical Architecture
* [cite_start]**Farmer Interface:** WhatsApp (using Meta Cloud API) 
* [cite_start]**Backend:** Flask (Python) 
* **Public Tunneling:** ngrok (for development)

## How to Run
1.  Clone the repository.
2.  Create a Python virtual environment: `python -m venv venv`
3.  Activate it: `venv\Scripts\activate`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Create a `.env` file based on the provided template and fill in your secrets.
6.  Run the Flask app: `python app.py`
7.  Run `ngrok` to create a public tunnel to port 5000.
8.  Configure the `ngrok` URL as the webhook in your Meta Developer App dashboard.
