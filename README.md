# WhatsApp Business Agent - After Hours Support

Een geavanceerde 24/7 WhatsApp agent die klantvragen beantwoordt na werkuren, productkennis heeft, en automatisch tickets aanmaakt wanneer escalatie nodig is.

## Wat deze agent kan

✅ **24/7 Klantondersteuning** via WhatsApp
✅ **Productkennis** - kent al je producten, prijzen, specificaties
✅ **Zelfstandig antwoorden** - lost vragen autonoom op
✅ **Slimme escalatie** - maakt tickets aan bij complexe vragen
✅ **Sentiment detection** - herkent gefrustreerde klanten
✅ **Meertalig** - Nederlands, Engels, Frans, Duits
✅ **Prioritering** - classificeert tickets op urgentie
✅ **Team handover** - bereidt next-day follow-up voor

## Verbeteringen t.o.v. basisidee

1. **Contextueel begrip**: Onthoudt conversatiegeschiedenis
2. **RAG (Retrieval Augmented Generation)**: Zoekt accurate productinfo
3. **Ticketprioritering**: Low/Medium/High/Urgent classificatie
4. **Automatische samenvattingen**: Genereert team-briefings
5. **Learning loop**: Slaat succesvolle oplossingen op
6. **Proactieve suggesties**: Biedt gerelateerde informatie aan
7. **Multi-intent herkenning**: Begrijpt complexe vragen

## Architectuur

```
WhatsApp → Twilio Webhook → Flask App → Agent Core
                                      ↓
                            [Vector Database]
                            [Product Knowledge]
                                      ↓
                            [LLM (OpenAI)]
                                      ↓
                         ┌────────────┴────────────┐
                         ↓                         ↓
                  [WhatsApp Response]      [Ticket System]
                                                 ↓
                                        [Team Dashboard]
```

## Installatie

### 1. Omgevingsvariabelen

```bash
cp .env.example .env
```

Vul `.env` in:

```env
# OpenAI API
OPENAI_API_KEY=sk-...

# Twilio
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Ticketing (optioneel)
TICKET_WEBHOOK_URL=https://your-ticket-system.com/api/tickets

# Bedrijfsinfo
COMPANY_NAME=JouwBedrijf
SUPPORT_EMAIL=support@jouwnbedrijf.nl
WORK_HOURS_START=9
WORK_HOURS_END=17
TIMEZONE=Europe/Amsterdam

# Server
FLASK_PORT=5000
HOST=0.0.0.0
```

### 2. Productdata toevoegen

Maak een `data/products/` directory en voeg toe:
- PDF catalogi
- Prijslijsten (.txt, .md, .csv)
- FAQ documenten
- Productspecificaties
- Website URLs

```bash
mkdir -p data/products
```

Voorbeeld bestanden:
- `product_catalog.pdf`
- `pricing_2025.md`
- `faq_general.txt`
- `specifications.csv`

### 3. Vector database initialiseren

```bash
python setup_vector_db.py
```

Dit indexeert al je productinformatie in ChromaDB.

### 4. Dependencies installeren

```bash
pip install -r requirements.txt
```

## Gebruik

### Server starten

```bash
python app.py
```

De server luistert op poort 5000 voor Twilio webhooks.

### Lokaal testen

```bash
python test_agent.py "Hoeveel kost de Premium Subscription?"
```

### Conversatie testen

```bash
python test_conversation.py
```

## Hoe het werkt

### Stap 1: Bericht ontvangen
- Klant stuurt WhatsApp bericht naar bedrijfsnummer
- Twilio forwardt naar `/webhook/whatsapp` endpoint

### Stap 2: Werkuren check
- Binnen werkuren? → Stuur door naar menselijke agent (optioneel)
- Na werkuren? → Activeer AI agent

### Stap 3: Intentie & Sentiment analyse
- Wat wil de klant? (vraag, klacht, bestelling, info)
- Hoe is de stemming? (positief, neutraal, gefrustreerd)

### Stap 4: Kennis ophalen (RAG)
- Zoek in vector database naar relevante productinfo
- Haal context uit knowledge base
- Combineer multiple bronnen

### Stap 5: Antwoord genereren
- LLM formuleert natuurlijk, behulpzaam antwoord
- Inclusief details: prijs, beschikbaarheid, specificaties
- Toon past zich aan aan sentiment

### Stap 6: Escalatie decision
**Kan de agent dit oplossen?**
- ✅ Ja → Stuur antwoord via WhatsApp
- ❌ Nee → Maak ticket aan

**Escalatie criteria:**
- Vraag te complex
- Klant ontevreden (negatief sentiment)
- Juridische/financiële kwesties
- Technische storingen
- Herhaalde vragen

### Stap 7: Ticket creatie

Ticket bevat:
```json
{
  "ticket_id": "TKT-20250109-001",
  "timestamp": "2025-01-09T22:15:00Z",
  "customer_phone": "+31612345678",
  "customer_name": "Jan Jansen",
  "question": "Kan ik product X retourneren na 30 dagen?",
  "conversation_history": [...],
  "sentiment": "neutral",
  "priority": "medium",
  "category": "returns",
  "suggested_action": "Check aankoopdatum, uitleggen beleid",
  "status": "open",
  "assigned_to": null
}
```

### Stap 8: Team notificatie
- Ticket opgeslagen in `tickets/open_tickets.json`
- Optioneel: Email naar team
- Dashboard update voor next-day review

## Bestandsstructuur

```
/workspace
├── app.py                  # Flask server + webhook handler
├── agent_core.py           # Agent logica, RAG, LLM calls
├── knowledge_base.py       # Vector search, document loading
├── ticket_system.py        # Ticket creatie & management
├── sentiment_analyzer.py   # Sentiment detection
├── setup_vector_db.py      # Database initialisatie
├── test_agent.py           # Test scripts
├── test_conversation.py    # Conversationele tests
├── requirements.txt        # Dependencies
├── .env.example            # Template voor env vars
├── README.md               # Deze documentatie
│
├── data/
│   └── products/           # Productdocumenten
│       ├── catalog.pdf
│       ├── pricing.md
│       └── faq.txt
│
├── vector_db/              # ChromaDB storage (auto-generated)
│
├── tickets/
│   ├── open_tickets.json   # Actieve tickets
│   └── resolved_tickets.json
│
└── logs/
    └── agent.log           # Logs en monitoring
```

## Configuratie opties

### Werkuren aanpassen

In `.env`:
```env
WORK_HOURS_START=9
WORK_HOURS_END=17
TIMEZONE=Europe/Amsterdam
WEEKEND_OFF=true  # Geen support in weekend
```

### Ticket systeem integratie

Gebruik ingebouwd JSON systeem:
```env
TICKET_STORAGE=json  # default
```

Of integreer met externe systemen:
```env
TICKET_STORAGE=webhook
TICKET_WEBHOOK_URL=https://api.zendesk.com/api/v2/tickets
TICKET_WEBHOOK_AUTH=Bearer your_token
```

### Aangepaste prompts

Bewerk prompts in `agent_core.py`:
- `SYSTEM_PROMPT`: Algemene instructies
- `ESCALATION_PROMPT`: Wanneer escaleren?
- `TONE_GUIDELINES`: Communicatiestijl

### Prioriteitsregels

Standaard prioritering:
- **Low**: Algemene info, openingstijden
- **Medium**: Productvragen, bestellingen
- **High**: Klachten, technische issues
- **Urgent**: Gefrustreerde klant, VIP, security

## Monitoring

### Logs bekijken

```bash
tail -f logs/agent.log
```

Log niveau aanpassen in `.env`:
```env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

### Tickets bekijken

Open tickets:
```bash
cat tickets/open_tickets.json | jq
```

Statistieken:
```bash
python analyze_tickets.py
```

### Performance metrics

- Response tijd
- Resolutie percentage
- Escalatie rate
- Klanttevredenheid (sentiment trend)

## Veiligheid

🔒 **API keys**: Via `.env`, nooit commiten
🔒 **Data privacy**: Telefoonnummers gemaskeerd in logs
🔒 **Rate limiting**: Voorkomt misbruik (10 berichten/minuut)
🔒 **Input validatie**: SQL injection, XSS preventie
🔒 **HTTPS**: Altijd versleuteld verkeer

## Voorbeeld conversaties

### Scenario 1: Productvraag

**Klant**: "Hoeveel kost de Enterprise licentie?"

**Agent**: 
```
De Enterprise licentie kost €299 per maand. 

Dit includes:
✓ Ongelimiteerde gebruikers
✓ 24/7 priority support
✓ Custom integraties
✓ Dedicated account manager

Wil je meer weten over de specifieke features of 
wil ik je doorverbinden met sales voor een demo?
```

### Scenario 2: Retourneren

**Klant**: "Ik wil mijn bestelling retourneren"

**Agent**:
```
Natuurlijk help ik je daarmee! 

Ons retourbeleid:
- Binnen 30 dagen na ontvangst
- Product moet ongebruikt zijn
- Originele verpakking vereist

Kan je je ordernummer delen? Dan kijk ik 
direct de status voor je na en stuur ik 
het retouretiket.
```

*(klant geeft geen ordernummer)*

**Agent**:
```
Geen probleem! Je kunt het ordernummer vinden in:
- Je bevestigingsmail
- Je account onder 'Bestellingen'
- Op de pakbon

Zodra je het nummer hebt, help ik je direct verder! 😊
```

### Scenario 3: Escalatie

**Klant**: "Dit is de derde keer dat het niet werkt! Ik wil mijn geld terug!"

**Agent**: 
```
Het spijt me zeer te horen dat je deze ervaring hebt. 
Ik begrijp je frustratie volledig.

Laat me dit direct escaleren naar ons customer success team. 
Zij nemen binnen 2 uur contact met je op om dit op te lossen.

Kan je kort beschrijven wat er precies misging? 
Dan zorg ik dat het team alle informatie heeft.
```

→ **Ticket aangemaakt** (Priority: HIGH, Sentiment: NEGATIVE)

## Uitbreidingen

### Kortetermijn
- [ ] CRM integratie (Salesforce, HubSpot)
- [ ] Voice support (Twilio Voice)
- [ ] Multi-channel (Messenger, Telegram)
- [ ] Betaallinks via WhatsApp

### Langetermijn
- [ ] Analytics dashboard (real-time)
- [ ] Auto-learning van feedback
- [ ] Voice-of-customer insights
- [ ] Predictive support (proactief)

## Testing

### Unit tests

```bash
pytest tests/
```

### Integration tests

```bash
python test_integration.py
```

### E2E test met Twilio sandbox

1. Activeer Twilio WhatsApp sandbox
2. Stuur testberichten
3. Monitor logs en tickets

## Troubleshooting

### Agent reageert niet

Check:
- Twilio webhook URL correct?
- Server draait (`python app.py`)?
- OPENAI_API_KEY geldig?
- Vector database geïnitialiseerd?

### Tickets worden niet aangemaakt

Check:
- `tickets/` directory bestaat en is writable?
- `ticket_system.py` import errors?
- Webhook URL bereikbaar (indien gebruikt)?

### Slechte antwoorden

Optimaliseer:
- Meer/betere productdocumenten toevoegen
- Prompts verfijnen in `agent_core.py`
- Temperature aanpassen (lager = consistenter)
- Few-shot examples toevoegen

## Ondersteuning

📧 Email: support@whatsapp-agent.dev  
📚 Documentatie: `/docs`  
🐛 Issues: GitHub Issues  
💡 Feature requests: Welkom!

---

**Ready to launch?** 🚀

1. ✅ Vul `.env` in
2. ✅ Voeg productdata toe
3. ✅ Run `python setup_vector_db.py`
4. ✅ Start `python app.py`
5. ✅ Configureer Twilio webhook
6. ✅ Test met WhatsApp bericht

Veel succes met je 24/7 support agent!
