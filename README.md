# Momentum Coach

Een eenvoudige persoonlijke Streamlit workout-app die je helpt om consistenter te trainen, fitter te worden en je voortgang zichtbaar te maken met de trainingsmiddelen die je thuis hebt.

## Wat deze eerste versie kan

- Persoonlijke dagelijkse workout op basis van:
  - kettlebell
  - dumbbell
  - mountainbike
  - lichaamsgewicht
- Dagelijkse workout-pagina met:
  - duur
  - tools
  - oefeningen
  - korte uitleg
  - motivatiebericht
- Slimmere varianten voor:
  - weinig energie
  - maar 15 minuten
  - geen zin vandaag
- Workout logging met:
  - gedaan of niet
  - zwaarte 1-10
  - energie 1-10
  - sets/reps notitie
  - gewicht
  - reflectie
- Dashboard met:
  - aantal workouts
  - streak
  - trainingen per week
  - laatste workout
  - gemiddelde energie
  - gemiddelde moeilijkheid
  - beste week
- Progressie-overzicht met trends per week
- Instellingen voor naam, doel, niveau, tijd en weekdoel

## Structuur

```text
app.py            # hoofdapp en UI
storage.py        # SQLite opslag en statistieken
workout_data.py   # workouts, badges en motivatielogica
requirements.txt  # dependencies
data/             # wordt automatisch aangemaakt voor de SQLite database
```

## Lokaal draaien

1. Maak een virtuele omgeving aan:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Installeer de dependencies:

```bash
pip install -r requirements.txt
```

3. Start de app:

```bash
streamlit run app.py
```

4. Open daarna de link die Streamlit in je terminal toont.

## Deployen via GitHub en Streamlit Community Cloud

1. Zet deze bestanden in een GitHub repository.
2. Zorg dat `app.py` in de root staat.
3. Zorg dat `requirements.txt` aanwezig is.
4. Push naar GitHub.
5. Ga naar [Streamlit Community Cloud](https://share.streamlit.io/).
6. Kies **New app**.
7. Selecteer je repository, branch en `app.py`.
8. Deploy de app.

## Handige volgende uitbreidingen

- echt persoonlijk weekschema op basis van gekozen trainingsdagen
- automatische meldingen of herinneringen
- progressief zwaardere weken
- aparte onboarding voor startgewicht en doelen
- export van logboek naar CSV
- oefenbibliotheek met demo-afbeeldingen of video-links
