# WhatsApp Business Agent - Core Implementation

from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
import pytz
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
COMPANY_NAME = os.getenv('COMPANY_NAME', 'YourCompany')
WORK_HOURS_START = int(os.getenv('WORK_HOURS_START', 9))
WORK_HOURS_END = int(os.getenv('WORK_HOURS_END', 17))
TIMEZONE = os.getenv('TIMEZONE', 'Europe/Amsterdam')


class WhatsAppAgent:
    """
    Main agent class that handles customer conversations
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not set. Agent will run in mock mode.")
        
    def is_within_work_hours(self):
        """Check if current time is within work hours"""
        tz = pytz.timezone(TIMEZONE)
        now = datetime.now(tz)
        
        # Check weekend
        if now.weekday() >= 5:  # Saturday=5, Sunday=6
            return False
        
        # Check work hours
        return WORK_HOURS_START <= now.hour < WORK_HOURS_END
    
    def analyze_sentiment(self, message):
        """Analyze sentiment of customer message"""
        negative_words = ['boos', 'frustratie', 'slecht', 'teleurgesteld', 
                         'probleem', 'klaag', 'niet werken', 'geld terug',
                         'angry', 'frustrated', 'bad', 'disappointed', 'problem']
        
        urgent_words = ['dringend', 'urgent', 'direct', 'nu', 'asap', 
                       'emergency', 'spoed']
        
        message_lower = message.lower()
        
        sentiment_score = 0
        urgency_score = 0
        
        for word in negative_words:
            if word in message_lower:
                sentiment_score -= 1
        
        for word in urgent_words:
            if word in message_lower:
                urgency_score += 1
        
        # Classify sentiment
        if sentiment_score <= -2:
            sentiment = 'negative'
        elif sentiment_score >= 1:
            sentiment = 'positive'
        else:
            sentiment = 'neutral'
        
        # Classify urgency
        if urgency_score >= 2:
            priority = 'high'
        elif urgency_score == 1:
            priority = 'medium'
        else:
            priority = 'low'
        
        return {
            'sentiment': sentiment,
            'priority': priority,
            'score': sentiment_score
        }
    
    def should_escalate(self, message, sentiment_analysis, can_answer):
        """Determine if ticket should be created"""
        
        if not can_answer:
            return True, 'unable_to_answer'
        
        if sentiment_analysis['sentiment'] == 'negative':
            return True, 'negative_sentiment'
        
        if sentiment_analysis['priority'] == 'high':
            return True, 'high_priority'
        
        return False, None
    
    def generate_response(self, message, context=None):
        """Generate response using LLM"""
        
        if not self.openai_api_key:
            return self._mock_response(message)
        
        try:
            from langchain_openai import ChatOpenAI
            from langchain.schema import HumanMessage, SystemMessage
            
            llm = ChatOpenAI(
                model='gpt-4',
                temperature=0.7,
                api_key=self.openai_api_key
            )
            
            system_prompt = f"""Je bent een behulpzame klantenservice agent voor {COMPANY_NAME}.
            
Jouw taken:
1. Beantwoord klantvragen vriendelijk en professioneel
2. Geef accurate informatie over producten en diensten
3. Wees behulpzaam en empathisch
4. Als je iets niet weet, geef dat eerlijk toe

Belangrijke richtlijnen:
- Houd antwoorden beknopt (max 300 woorden)
- Gebruik emoji's waar passend 😊
- Bied altijd vervolghulp aan
- Verwijs niet naar AI of dat je een bot bent

Als de vraag te complex is, zeg dan: "Laat me dit navragen bij ons team. Zij nemen binnen 2 uur contact met je op."
"""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=message)
            ]
            
            if context:
                messages.insert(1, HumanMessage(content=f"Context: {context}"))
            
            response = llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._mock_response(message)
    
    def _mock_response(self, message):
        """Mock response for testing without API key"""
        
        message_lower = message.lower()
        
        if 'prijs' in message_lower or 'kost' in message_lower:
            return "Onze prijzen variëren per product. Kun je specificeren welk product je interesseert? Ik help je graag met de juiste informatie! 💰"
        
        elif 'openingstijd' in message_lower or 'open' in message_lower:
            return f"Wij zijn geopend van {WORK_HOURS_START}:00 tot {WORK_HOURS_END}:00 op werkdagen. Na deze tijden help ik je graag hier! 🕐"
        
        elif 'contact' in message_lower or 'bellen' in message_lower:
            return "Je kunt ons bereiken via:\n📧 Email: support@company.com\n📞 Telefoon: +31 20 1234567\n\nWaar kan ik je verder mee helpen?"
        
        elif 'retour' in message_lower or 'terugsturen' in message_lower:
            return "Ons retourbeleid:\n✅ Binnen 30 dagen\n✅ Product ongebruikt\n✅ Originele verpakking\n\nHeb je je ordernummer bij de hand? Dan help ik je direct verder!"
        
        elif 'levering' in message_lower or 'verzending' in message_lower:
            return "Levering gebeurt binnen 2-3 werkdagen. Je ontvangt een track & trace code zodra je pakket verzonden is. 📦\n\nWil je de status van een bestelling checken?"
        
        else:
            return "Bedankt voor je bericht! Ik help je graag. Kun je wat meer details geven over je vraag? Dan kan ik je beter assisteren! 😊"


# Initialize agent
agent = WhatsAppAgent()


@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages"""
    
    try:
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        to_number = request.values.get('To', '')
        
        if not incoming_msg:
            logger.warning("Empty message received")
            return jsonify({'error': 'No message body'}), 400
        
        logger.info(f"Message from {from_number}: {incoming_msg[:100]}...")
        
        if agent.is_within_work_hours():
            logger.info("Within work hours, but AI responding")
        
        sentiment = agent.analyze_sentiment(incoming_msg)
        logger.info(f"Sentiment: {sentiment}")
        
        response_text = agent.generate_response(incoming_msg)
        
        should_esc, reason = agent.should_escalate(
            incoming_msg, 
            sentiment, 
            can_answer=True
        )
        
        if should_esc:
            logger.info(f"Escalating ticket. Reason: {reason}")
            from ticket_system import create_ticket
            ticket = create_ticket(
                customer_phone=from_number,
                question=incoming_msg,
                sentiment=sentiment,
                conversation_history=[incoming_msg],
                reason=reason
            )
            logger.info(f"Ticket created: {ticket.get('ticket_id')}")
            
            if sentiment['sentiment'] == 'negative':
                response_text = (
                    "Het spijt me te horen dat je deze ervaring hebt. "
                    "Ik begrijp je frustratie.\n\n"
                    "Ik heb je vraag geëscaleerd naar ons specialistische team. "
                    "Zij nemen binnen 2 uur contact met je op om dit op te lossen.\n\n"
                    "Kan je nog kort beschrijven wat er precies misging? "
                    "Dan heeft het team alle informatie. 🙏"
                )
            else:
                response_text = (
                    "Bedankt voor je vraag! Dit is een specifieke kwestie die ik graag "
                    "door ons team laat bekijken.\n\n"
                    "Zij nemen morgen tijdens kantoortijden contact met je op met een antwoord. "
                    "Is dat goed? 😊"
                )
        
        resp = MessagingResponse()
        resp.message(response_text)
        
        logger.info(f"Response sent to {from_number}")
        
        return str(resp)
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        resp = MessagingResponse()
        resp.message("Excuses, er ging iets mis. Probeer het opnieuw of bel ons direct.")
        return str(resp)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'work_hours': agent.is_within_work_hours()
    })


@app.route('/test', methods=['POST'])
def test_agent():
    """Test endpoint for local testing"""
    message = request.json.get('message', '')
    from_number = request.json.get('from_number', '+31612345678')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = agent.generate_response(message)
    sentiment = agent.analyze_sentiment(message)
    
    return jsonify({
        'message': message,
        'response': response,
        'sentiment': sentiment,
        'work_hours': agent.is_within_work_hours()
    })


if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    logger.info(f"Starting WhatsApp Agent server on {host}:{port}")
    app.run(host=host, port=port, debug=True)
