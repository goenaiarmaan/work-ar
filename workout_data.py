from __future__ import annotations

from datetime import date


MOTIVATION_QUOTES = [
    "Vandaag niet perfect, maar wel opdagen.",
    "Discipline wint het van motivatie op de dagen dat je geen zin hebt.",
    "Kleine sessies bouwen grote resultaten.",
    "Je hoeft niet te pieken. Je hoeft alleen te verschijnen.",
    "Sterker worden begint met nog een herhaling.",
    "Rustig, strak, consistent. Dat is hoe progressie eruitziet.",
    "Je lichaam luistert naar wat je vaak doet.",
]


BADGES = [
    (3, "Starter", "Je bent begonnen. Dat is waar momentum ontstaat."),
    (7, "7-Dagen Reeks", "Een volle week van opdagen."),
    (15, "Consistent", "Je bouwt een echte routine op."),
    (25, "Sterke Basis", "Je discipline begint zichtbaar te worden."),
    (40, "Machine", "Je komt opdagen, ook als het niet makkelijk is."),
]


WORKOUT_LIBRARY = {
    "full_body_strength": {
        "title": "Full Body Strength",
        "type": "Kracht",
        "duration": 35,
        "difficulty": "Beginner-Intermediate",
        "tools": ["Kettlebell", "Dumbbell", "Lichaamsgewicht"],
        "focus": ["Kracht", "Vetverlies", "Conditie"],
        "exercises": [
            {"name": "Kettlebell swings", "prescription": "3 sets van 15", "note": "Explosief vanuit de heupen, rug neutraal."},
            {"name": "Dumbbell rows", "prescription": "3 sets van 12 per arm", "note": "Trek je elleboog richting je heup."},
            {"name": "Push-ups", "prescription": "3 sets tot nette techniek stopt", "note": "Span je buik aan en houd je lichaam recht."},
            {"name": "Goblet squats", "prescription": "3 sets van 12", "note": "Zak gecontroleerd en duw krachtig omhoog."},
            {"name": "Plank", "prescription": "3 rondes van 30-45 seconden", "note": "Ribben laag, billen aangespannen."},
        ],
    },
    "kettlebell_conditioning": {
        "title": "Kettlebell Conditioning",
        "type": "Conditioning",
        "duration": 28,
        "difficulty": "Beginner-Intermediate",
        "tools": ["Kettlebell", "Lichaamsgewicht"],
        "focus": ["Conditie", "Vetverlies"],
        "exercises": [
            {"name": "Kettlebell swings", "prescription": "5 rondes van 20", "note": "Rust 45 seconden tussen de rondes."},
            {"name": "Reverse lunges", "prescription": "4 sets van 10 per been", "note": "Blijf lang in je romp."},
            {"name": "Mountain climbers", "prescription": "4 sets van 30 seconden", "note": "Werk snel maar gecontroleerd."},
            {"name": "Kettlebell deadlift", "prescription": "3 sets van 12", "note": "Heupen naar achter, borst open."},
        ],
    },
    "dumbbell_strength": {
        "title": "Dumbbell Strength",
        "type": "Kracht",
        "duration": 32,
        "difficulty": "Beginner-Intermediate",
        "tools": ["Dumbbell", "Lichaamsgewicht"],
        "focus": ["Kracht", "Spieruithoudingsvermogen"],
        "exercises": [
            {"name": "Dumbbell floor press", "prescription": "4 sets van 10", "note": "Laat je bovenarmen kort de vloer raken."},
            {"name": "Dumbbell Romanian deadlift", "prescription": "4 sets van 12", "note": "Voel de rek op je hamstrings."},
            {"name": "One-arm dumbbell row", "prescription": "3 sets van 12 per arm", "note": "Stabiele romp, geen rukbeweging."},
            {"name": "Split squats", "prescription": "3 sets van 10 per been", "note": "Zak recht omlaag."},
            {"name": "Dead bug", "prescription": "3 sets van 10 per kant", "note": "Onderrug blijft rustig tegen de grond."},
        ],
    },
    "core_workout": {
        "title": "Core Reset",
        "type": "Core",
        "duration": 20,
        "difficulty": "Beginner",
        "tools": ["Lichaamsgewicht"],
        "focus": ["Core", "Stabiliteit", "Herstel"],
        "exercises": [
            {"name": "Dead bug", "prescription": "3 sets van 10 per kant", "note": "Werk langzaam en gecontroleerd."},
            {"name": "Side plank", "prescription": "3 sets van 20-30 seconden per kant", "note": "Heupen hoog."},
            {"name": "Bird dog", "prescription": "3 sets van 8 per kant", "note": "Houd je bekken stil."},
            {"name": "Glute bridge", "prescription": "3 sets van 15", "note": "Duw uit je hielen."},
        ],
    },
    "fat_loss_circuit": {
        "title": "Fat Loss Circuit",
        "type": "Circuit",
        "duration": 25,
        "difficulty": "Beginner-Intermediate",
        "tools": ["Kettlebell", "Dumbbell", "Lichaamsgewicht"],
        "focus": ["Vetverlies", "Conditie"],
        "exercises": [
            {"name": "Squats", "prescription": "40 seconden werk / 20 seconden rust", "note": "Blijf in ritme."},
            {"name": "Push-ups", "prescription": "40 seconden werk / 20 seconden rust", "note": "Maak ze desnoods op een verhoging."},
            {"name": "Kettlebell swings", "prescription": "40 seconden werk / 20 seconden rust", "note": "Explosieve heupen."},
            {"name": "Dumbbell rows", "prescription": "40 seconden werk / 20 seconden rust", "note": "Wissel armen halverwege."},
            {"name": "High knees", "prescription": "40 seconden werk / 20 seconden rust", "note": "Lichte, snelle voeten."},
        ],
    },
    "mountainbike_cardio": {
        "title": "Mountainbike Cardio Day",
        "type": "Cardio",
        "duration": 45,
        "difficulty": "Beginner-Intermediate",
        "tools": ["Mountainbike"],
        "focus": ["Conditie", "Vetverlies", "Energie"],
        "exercises": [
            {"name": "Rustig inrijden", "prescription": "10 minuten", "note": "Bouw je ademhaling rustig op."},
            {"name": "Tempo blokken", "prescription": "5 x 3 minuten stevig / 2 minuten rustig", "note": "Stevig, maar houd controle."},
            {"name": "Uitrijden", "prescription": "10 minuten", "note": "Laat je hartslag zakken."},
        ],
    },
    "recovery_mobility": {
        "title": "Recovery & Mobility",
        "type": "Herstel",
        "duration": 18,
        "difficulty": "Beginner",
        "tools": ["Lichaamsgewicht"],
        "focus": ["Mobiliteit", "Herstel", "Energie"],
        "exercises": [
            {"name": "World's greatest stretch", "prescription": "2 rondes per kant", "note": "Adem diep in elke positie."},
            {"name": "Hip openers", "prescription": "2 sets van 45 seconden per kant", "note": "Geen haast."},
            {"name": "Thoracic rotations", "prescription": "2 sets van 8 per kant", "note": "Open je borst."},
            {"name": "Child's pose breathing", "prescription": "2 minuten", "note": "Langzame ademhaling."},
        ],
    },
    "quick_15": {
        "title": "Quick 15",
        "type": "Snel",
        "duration": 15,
        "difficulty": "Beginner",
        "tools": ["Kettlebell", "Dumbbell", "Lichaamsgewicht"],
        "focus": ["Consistentie", "Energie"],
        "exercises": [
            {"name": "Bodyweight squats", "prescription": "3 sets van 20", "note": "Vloeiend tempo."},
            {"name": "Push-ups", "prescription": "3 sets van 8-12", "note": "Kies een variant die netjes blijft."},
            {"name": "Kettlebell deadlift", "prescription": "3 sets van 15", "note": "Kracht uit je heupen."},
            {"name": "Plank", "prescription": "3 sets van 30 seconden", "note": "Kort, strak en gefocust."},
        ],
    },
    "show_up": {
        "title": "Show Up Session",
        "type": "Minimum dose",
        "duration": 10,
        "difficulty": "Beginner",
        "tools": ["Lichaamsgewicht"],
        "focus": ["Discipline", "Momentum"],
        "exercises": [
            {"name": "Walk in place", "prescription": "2 minuten", "note": "Breng je lichaam op gang."},
            {"name": "Air squats", "prescription": "2 sets van 15", "note": "Rustig ritme."},
            {"name": "Incline push-ups of wall push-ups", "prescription": "2 sets van 10", "note": "Maak het haalbaar."},
            {"name": "Plank", "prescription": "2 sets van 20 seconden", "note": "Kort en scherp."},
        ],
    },
}


WEEKLY_PATTERN = {
    0: "full_body_strength",
    1: "mountainbike_cardio",
    2: "dumbbell_strength",
    3: "recovery_mobility",
    4: "kettlebell_conditioning",
    5: "fat_loss_circuit",
    6: "core_workout",
}


def motivation_for_day(target_date: date) -> str:
    return MOTIVATION_QUOTES[target_date.toordinal() % len(MOTIVATION_QUOTES)]


def get_workout(workout_key: str) -> dict:
    return WORKOUT_LIBRARY[workout_key]


def scale_workout(workout: dict, mode: str) -> dict:
    scaled = {**workout, "exercises": [exercise.copy() for exercise in workout["exercises"]]}

    if mode == "low_energy":
        scaled["duration"] = max(12, workout["duration"] - 10)
        for exercise in scaled["exercises"]:
            exercise["prescription"] = f"Lichter: {exercise['prescription']}"
        scaled["coach_note"] = "Lage energie is geen reden om te stoppen. Vandaag houden we het bewust lichter."
    elif mode == "quick":
        return {**WORKOUT_LIBRARY["quick_15"], "coach_note": "Drukke dag. Kort trainen telt nog steeds."}
    elif mode == "show_up":
        return {**WORKOUT_LIBRARY["show_up"], "coach_note": "Geen zin? Prima. We kiezen de kleinste stap die telt."}
    elif mode == "high_energy":
        scaled["duration"] = workout["duration"] + 8
        scaled["coach_note"] = "Je energie is hoog. Vandaag mag je iets harder duwen, zonder je techniek te verliezen."
    else:
        scaled["coach_note"] = "Rustig opbouwen, netjes bewegen, en vandaag gewoon leveren."

    return scaled


def pick_workout_for_date(target_date: date, energy_mode: str = "normal", available_minutes: int = 30) -> dict:
    base_key = WEEKLY_PATTERN[target_date.weekday()]
    workout = get_workout(base_key)

    if available_minutes <= 15:
        return scale_workout(workout, "quick")
    if energy_mode == "show_up":
        return scale_workout(workout, "show_up")
    if energy_mode == "low":
        return scale_workout(workout, "low_energy")
    if energy_mode == "high":
        return scale_workout(workout, "high_energy")
    return scale_workout(workout, "normal")
