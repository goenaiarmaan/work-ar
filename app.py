from __future__ import annotations

from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st

from storage import add_log, dashboard_stats, fetch_logs, fetch_logs_in_range, get_settings, init_db, save_settings
from workout_data import BADGES, motivation_for_day, pick_workout_for_date


st.set_page_config(
    page_title="Momentum Coach",
    page_icon="💪",
    layout="wide",
)

init_db()


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --bg: #f3efe5;
                --panel: rgba(255, 251, 244, 0.92);
                --panel-strong: #fffaf1;
                --text: #1f2a1f;
                --muted: #617164;
                --accent: #1f6f5f;
                --accent-soft: #dceee4;
                --warm: #d9802e;
                --border: rgba(31, 42, 31, 0.10);
            }
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(217, 128, 46, 0.18), transparent 28%),
                    radial-gradient(circle at top right, rgba(31, 111, 95, 0.16), transparent 26%),
                    linear-gradient(180deg, #f6f0e4 0%, #efe6d7 100%);
                color: var(--text);
            }
            h1, h2, h3 {
                color: var(--text);
                letter-spacing: -0.02em;
            }
            .block-card {
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 20px;
                padding: 1.1rem 1.2rem;
                box-shadow: 0 14px 40px rgba(57, 65, 49, 0.08);
            }
            .hero {
                background: linear-gradient(135deg, rgba(31,111,95,0.95), rgba(26,76,64,0.95));
                color: #f9f5ef;
                border-radius: 24px;
                padding: 1.4rem 1.5rem;
                box-shadow: 0 18px 42px rgba(20, 50, 44, 0.22);
            }
            .mini-label {
                text-transform: uppercase;
                font-size: 0.76rem;
                letter-spacing: 0.09em;
                color: var(--muted);
            }
            .quote {
                background: rgba(255, 250, 241, 0.76);
                border-left: 6px solid var(--warm);
                border-radius: 14px;
                padding: 1rem 1.1rem;
                color: var(--text);
            }
            .exercise {
                background: var(--panel-strong);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 0.9rem 1rem;
                margin-bottom: 0.8rem;
            }
            .badge {
                display: inline-block;
                padding: 0.45rem 0.75rem;
                background: var(--accent-soft);
                color: var(--accent);
                border-radius: 999px;
                margin: 0.2rem 0.35rem 0.2rem 0;
                font-weight: 600;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(settings: dict) -> None:
    today_text = date.today().strftime("%A %d %B %Y")
    st.markdown(
        f"""
        <div class="hero">
            <div class="mini-label">Momentum Coach</div>
            <h1 style="margin: 0.2rem 0 0.5rem 0;">{settings["name"]}, vandaag bouwen we momentum.</h1>
            <p style="margin: 0; font-size: 1.05rem;">
                Focus: {settings["goal"]}. Niet wachten op motivatie, maar slim en consistent trainen met wat je thuis hebt.
            </p>
            <p style="margin-top: 0.7rem; opacity: 0.9;">{today_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_today_workout(settings: dict) -> dict:
    mode_map = {
        "Laag": "low",
        "Normaal": "normal",
        "Hoog": "high",
    }
    energy_mode = mode_map.get(settings["energy_today"], "normal")
    minutes = int(settings["preferred_minutes"])

    if st.session_state.get("quick_mode"):
        return pick_workout_for_date(date.today(), "normal", 15)
    if st.session_state.get("show_up_mode"):
        return pick_workout_for_date(date.today(), "show_up", minutes)
    return pick_workout_for_date(date.today(), energy_mode, minutes)


def render_metrics(stats: dict, target: int) -> None:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Workouts voltooid", stats["completed_count"])
    col2.metric("Huidige streak", f'{stats["streak"]} dagen')
    col3.metric("Deze week", f'{stats["weekly_count"]}/{target} dagen')
    col4.metric("Beste week", f'{stats["best_week"]} trainingen')


def render_dashboard(settings: dict) -> None:
    stats = dashboard_stats()
    render_metrics(stats, int(settings["weekly_target"]))

    progress_ratio = min(stats["weekly_count"] / max(int(settings["weekly_target"]), 1), 1.0)
    st.progress(progress_ratio, text=f"Weekdoel: {stats['weekly_count']} van {settings['weekly_target']} trainingen")

    left, right = st.columns([1.3, 1])
    with left:
        st.markdown('<div class="block-card">', unsafe_allow_html=True)
        st.subheader("Coach-overzicht")
        st.write(f"Laatste workout: **{stats['latest_workout']}**")
        st.write(f"Gemiddelde energie: **{stats['avg_energy'] or '-'} / 10**")
        st.write(f"Gemiddelde zwaarte: **{stats['avg_difficulty'] or '-'} / 10**")
        if stats["latest_weight"] is not None:
            st.write(f"Laatst gelogd gewicht: **{stats['latest_weight']} kg**")
        st.write("Focus van deze app: opdagen, slim trainen en je voortgang zichtbaar maken.")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="block-card">', unsafe_allow_html=True)
        st.subheader("Badges")
        unlocked = [badge for badge in BADGES if stats["completed_count"] >= badge[0]]
        if unlocked:
            for _, title, desc in unlocked:
                st.markdown(f'<span class="badge">{title}</span>', unsafe_allow_html=True)
                st.caption(desc)
        else:
            st.write("Je eerste badge ligt klaar na 3 workouts.")
        st.markdown("</div>", unsafe_allow_html=True)

    recent_logs = fetch_logs(limit=8)
    if recent_logs:
        frame = pd.DataFrame(recent_logs)
        frame["log_date"] = pd.to_datetime(frame["log_date"])
        summary = frame.groupby(frame["log_date"].dt.date)["completed"].sum().reset_index()
        summary.columns = ["Datum", "Trainingen"]
        st.subheader("Recent ritme")
        st.line_chart(summary.set_index("Datum"))


def render_today(settings: dict) -> None:
    st.session_state.setdefault("quick_mode", False)
    st.session_state.setdefault("show_up_mode", False)

    button_col1, button_col2 = st.columns(2)
    if button_col1.button("Ik heb maar 15 minuten", use_container_width=True):
        st.session_state["quick_mode"] = True
        st.session_state["show_up_mode"] = False
    if button_col2.button("Geen zin vandaag", use_container_width=True):
        st.session_state["show_up_mode"] = True
        st.session_state["quick_mode"] = False

    workout = get_today_workout(settings)

    st.markdown('<div class="block-card">', unsafe_allow_html=True)
    st.subheader(f"Vandaag: {workout['title']}")
    st.write(f"**Duur:** {workout['duration']} minuten")
    st.write(f"**Tools:** {', '.join(workout['tools'])}")
    st.write(f"**Niveau:** {workout['difficulty']}")
    st.write(f"**Focus:** {', '.join(workout['focus'])}")
    st.info(workout["coach_note"])
    st.markdown("</div>", unsafe_allow_html=True)

    if settings.get("show_quotes", True):
        st.markdown(
            f'<div class="quote"><strong>Motivatie van de dag</strong><br>{motivation_for_day(date.today())}</div>',
            unsafe_allow_html=True,
        )

    st.subheader("Oefeningen")
    for exercise in workout["exercises"]:
        st.markdown(
            f"""
            <div class="exercise">
                <strong>{exercise["name"]}</strong><br>
                {exercise["prescription"]}<br>
                <span style="color:#617164;">{exercise["note"]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Workout loggen")
    with st.form("log_workout"):
        completed = st.checkbox("Ik heb deze workout gedaan", value=True)
        difficulty_score = st.slider("Hoe zwaar voelde het?", 1, 10, 6)
        achieved_text = st.text_input("Sets/reps gehaald", placeholder="Bijv. alle sets gehaald, laatste plank 25 sec")
        energy_score = st.slider("Energielevel na de training", 1, 10, 7)
        mood = st.selectbox("Hoe voelde je je mentaal?", ["Scherp", "Oké", "Moe", "Trots", "Moest mezelf duwen"])
        body_weight = st.number_input("Gewicht (optioneel)", min_value=0.0, step=0.1, value=0.0)
        note = st.text_area("Korte notitie", placeholder="Wat ging goed, wat was lastig, waar wil je op letten?")
        submitted = st.form_submit_button("Sla workout op", use_container_width=True)

        if submitted:
            add_log(
                {
                    "log_date": date.today().isoformat(),
                    "workout_title": workout["title"],
                    "workout_type": workout["type"],
                    "duration_minutes": workout["duration"],
                    "completed": completed,
                    "difficulty_score": difficulty_score,
                    "achieved_text": achieved_text,
                    "energy_score": energy_score,
                    "note": note,
                    "body_weight": body_weight if body_weight > 0 else None,
                    "mood": mood,
                }
            )
            st.success("Workout opgeslagen. Consistentie telt.")
            st.session_state["quick_mode"] = False
            st.session_state["show_up_mode"] = False


def render_logbook() -> None:
    st.subheader("Workout-logboek")
    logs = fetch_logs()
    if not logs:
        st.write("Nog geen trainingen gelogd.")
        return

    frame = pd.DataFrame(logs)
    frame["completed"] = frame["completed"].map({1: "Ja", 0: "Nee"})
    frame = frame.rename(
        columns={
            "log_date": "Datum",
            "workout_title": "Workout",
            "workout_type": "Type",
            "duration_minutes": "Minuten",
            "completed": "Gedaan",
            "difficulty_score": "Zwaarte",
            "achieved_text": "Resultaat",
            "energy_score": "Energie",
            "note": "Notitie",
            "body_weight": "Gewicht",
            "mood": "Mood",
        }
    )
    st.dataframe(frame[["Datum", "Workout", "Type", "Minuten", "Gedaan", "Zwaarte", "Energie", "Gewicht", "Mood", "Resultaat", "Notitie"]], use_container_width=True)


def render_progress() -> None:
    st.subheader("Progressie-overzicht")
    end = date.today()
    start = end - timedelta(days=60)
    logs = fetch_logs_in_range(start, end)
    if not logs:
        st.write("Log een paar workouts om je progressie hier te zien.")
        return

    frame = pd.DataFrame(logs)
    frame["log_date"] = pd.to_datetime(frame["log_date"])

    weekly = frame.groupby(frame["log_date"].dt.to_period("W")).agg(
        trainingen=("completed", "sum"),
        energie=("energy_score", "mean"),
        zwaarte=("difficulty_score", "mean"),
    ).reset_index()
    weekly["week"] = weekly["log_date"].astype(str)

    col1, col2 = st.columns(2)
    with col1:
        st.write("Trainingen per week")
        st.bar_chart(weekly.set_index("week")["trainingen"])
    with col2:
        st.write("Gemiddelde energie en zwaarte")
        st.line_chart(weekly.set_index("week")[["energie", "zwaarte"]])

    weight_rows = frame.dropna(subset=["body_weight"])
    if not weight_rows.empty:
        st.write("Gewichtstrend")
        weights = weight_rows[["log_date", "body_weight"]].rename(columns={"log_date": "Datum", "body_weight": "Gewicht"})
        st.line_chart(weights.set_index("Datum"))

    st.subheader("Weekly review")
    last_14 = frame[frame["log_date"] >= pd.Timestamp(datetime.now() - timedelta(days=14))]
    completed = int(last_14["completed"].sum())
    avg_energy = round(last_14["energy_score"].mean(), 1) if not last_14["energy_score"].dropna().empty else "-"
    avg_difficulty = round(last_14["difficulty_score"].mean(), 1) if not last_14["difficulty_score"].dropna().empty else "-"
    st.write(f"In de afgelopen 14 dagen deed je **{completed}** trainingen.")
    st.write(f"Gemiddelde energie: **{avg_energy} / 10**")
    st.write(f"Gemiddelde zwaarte: **{avg_difficulty} / 10**")
    st.write("Reflectievraag: welke gewoonte hielp je deze periode het meest om toch te trainen?")


def render_settings(settings: dict) -> dict:
    st.subheader("Instellingen")
    with st.form("settings_form"):
        name = st.text_input("Jouw naam of coach-naam", value=settings["name"])
        goal = st.text_input("Doel", value=settings["goal"])
        level = st.selectbox("Niveau", ["Beginner", "Beginner-Intermediate", "Intermediate"], index=["Beginner", "Beginner-Intermediate", "Intermediate"].index(settings["level"]))
        preferred_minutes = st.slider("Beschikbare tijd per dag", 10, 60, int(settings["preferred_minutes"]), 5)
        weekly_target = st.slider("Doel: trainingen per week", 2, 7, int(settings["weekly_target"]))
        energy_today = st.selectbox("Verwachte energie vandaag", ["Laag", "Normaal", "Hoog"], index=["Laag", "Normaal", "Hoog"].index(settings["energy_today"]))
        show_quotes = st.checkbox("Toon motivatiebericht", value=bool(settings.get("show_quotes", True)))
        saved = st.form_submit_button("Instellingen opslaan", use_container_width=True)
        if saved:
            settings = {
                "name": name,
                "goal": goal,
                "level": level,
                "preferred_minutes": preferred_minutes,
                "weekly_target": weekly_target,
                "energy_today": energy_today,
                "show_quotes": show_quotes,
            }
            save_settings(settings)
            st.success("Instellingen opgeslagen.")
            return settings
    return settings


def main() -> None:
    inject_styles()
    settings = get_settings()
    render_header(settings)

    page = st.sidebar.radio(
        "Ga naar",
        ["Dashboard", "Vandaag", "Logboek", "Progressie", "Instellingen"],
    )
    st.sidebar.caption("Train slim. Verschijn vaak. Bouw momentum.")

    if page == "Dashboard":
        render_dashboard(settings)
    elif page == "Vandaag":
        render_today(settings)
    elif page == "Logboek":
        render_logbook()
    elif page == "Progressie":
        render_progress()
    elif page == "Instellingen":
        render_settings(settings)


if __name__ == "__main__":
    main()
