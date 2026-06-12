from __future__ import annotations

import json
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path


APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
DB_PATH = DATA_DIR / "workout_app.db"

DEFAULT_SETTINGS = {
    "name": "Atleet in opbouw",
    "goal": "Fitter, sterker en consistenter worden",
    "level": "Beginner-Intermediate",
    "preferred_minutes": 30,
    "weekly_target": 4,
    "energy_today": "Normaal",
    "show_quotes": True,
}


def connect() -> sqlite3.Connection:
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workout_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date TEXT NOT NULL,
            workout_title TEXT NOT NULL,
            workout_type TEXT NOT NULL,
            duration_minutes INTEGER,
            completed INTEGER NOT NULL,
            difficulty_score INTEGER,
            achieved_text TEXT,
            energy_score INTEGER,
            note TEXT,
            body_weight REAL,
            mood TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()

    for key, value in DEFAULT_SETTINGS.items():
        cursor.execute(
            "INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)",
            (key, json.dumps(value)),
        )
    conn.commit()
    conn.close()


def get_settings() -> dict:
    conn = connect()
    rows = conn.execute("SELECT key, value FROM settings").fetchall()
    conn.close()
    settings = DEFAULT_SETTINGS.copy()
    for row in rows:
        settings[row["key"]] = json.loads(row["value"])
    return settings


def save_settings(settings: dict) -> None:
    conn = connect()
    cursor = conn.cursor()
    for key, value in settings.items():
        cursor.execute(
            "INSERT INTO settings(key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, json.dumps(value)),
        )
    conn.commit()
    conn.close()


def add_log(entry: dict) -> None:
    conn = connect()
    conn.execute(
        """
        INSERT INTO workout_logs(
            log_date, workout_title, workout_type, duration_minutes, completed,
            difficulty_score, achieved_text, energy_score, note, body_weight, mood, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            entry["log_date"],
            entry["workout_title"],
            entry["workout_type"],
            entry.get("duration_minutes"),
            1 if entry["completed"] else 0,
            entry.get("difficulty_score"),
            entry.get("achieved_text"),
            entry.get("energy_score"),
            entry.get("note"),
            entry.get("body_weight"),
            entry.get("mood"),
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()
    conn.close()


def fetch_logs(limit: int | None = None) -> list[dict]:
    conn = connect()
    query = "SELECT * FROM workout_logs ORDER BY log_date DESC, id DESC"
    if limit:
        query += f" LIMIT {int(limit)}"
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def fetch_logs_in_range(start_date: date, end_date: date) -> list[dict]:
    conn = connect()
    rows = conn.execute(
        """
        SELECT * FROM workout_logs
        WHERE log_date BETWEEN ? AND ?
        ORDER BY log_date ASC, id ASC
        """,
        (start_date.isoformat(), end_date.isoformat()),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def workout_days_this_week() -> int:
    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return sum(1 for row in fetch_logs_in_range(start, end) if row["completed"])


def current_streak() -> int:
    logs = [row for row in fetch_logs() if row["completed"]]
    logged_dates = sorted({datetime.fromisoformat(row["log_date"]).date() for row in logs}, reverse=True)
    if not logged_dates:
        return 0

    streak = 0
    cursor = date.today()
    logged_set = set(logged_dates)

    while cursor in logged_set:
        streak += 1
        cursor -= timedelta(days=1)

    if streak == 0 and (date.today() - timedelta(days=1)) in logged_set:
        cursor = date.today() - timedelta(days=1)
        while cursor in logged_set:
            streak += 1
            cursor -= timedelta(days=1)
    return streak


def dashboard_stats() -> dict:
    logs = fetch_logs()
    completed = [row for row in logs if row["completed"]]
    weights = [row["body_weight"] for row in logs if row["body_weight"] is not None]
    energy_scores = [row["energy_score"] for row in completed if row["energy_score"]]
    difficulty_scores = [row["difficulty_score"] for row in completed if row["difficulty_score"]]
    weekly_count = workout_days_this_week()

    weeks: dict[str, int] = {}
    for row in completed:
        log_day = datetime.fromisoformat(row["log_date"]).date()
        week_key = f"{log_day.isocalendar().year}-W{log_day.isocalendar().week:02d}"
        weeks[week_key] = weeks.get(week_key, 0) + 1

    best_week = max(weeks.values()) if weeks else 0
    latest = completed[0] if completed else None

    return {
        "completed_count": len(completed),
        "streak": current_streak(),
        "weekly_count": weekly_count,
        "latest_workout": latest["workout_title"] if latest else "Nog geen workout gelogd",
        "avg_energy": round(sum(energy_scores) / len(energy_scores), 1) if energy_scores else 0,
        "avg_difficulty": round(sum(difficulty_scores) / len(difficulty_scores), 1) if difficulty_scores else 0,
        "best_week": best_week,
        "latest_weight": weights[0] if weights else None,
    }
