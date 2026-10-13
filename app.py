"""Hospital management — Flask + SQLite.

Uses SQLite (hospital.db). Patients, doctors, and appointment booking with only an
exact same-start clash check (no 30-minute overlap handling). No search/billing.
"""

import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)
DB = "hospital.db"


def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS patient(
            id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT);
        CREATE TABLE IF NOT EXISTS doctor(
            id INTEGER PRIMARY KEY, name TEXT, specialization TEXT, fee REAL);
        CREATE TABLE IF NOT EXISTS appointment(
            id INTEGER PRIMARY KEY, patient_id INTEGER, doctor_id INTEGER,
            start_time TEXT, status TEXT DEFAULT 'booked');
        """
    )
    conn.commit(); conn.close()


@app.route("/api/patients", methods=["GET", "POST"])
def patients():
    conn = db()
    if request.method == "POST":
        d = request.get_json() or {}
        conn.execute("INSERT INTO patient(name,phone,email) VALUES(?,?,?)",
                     (d.get("name"), d.get("phone"), d.get("email")))
        conn.commit(); conn.close(); return jsonify({"ok": True}), 201
    rows = [dict(r) for r in conn.execute("SELECT * FROM patient")]
    conn.close(); return jsonify(rows)


@app.route("/api/doctors", methods=["GET", "POST"])
def doctors():
    conn = db()
    if request.method == "POST":
        d = request.get_json() or {}
        conn.execute("INSERT INTO doctor(name,specialization,fee) VALUES(?,?,?)",
                     (d.get("name"), d.get("specialization"), d.get("fee", 0)))
        conn.commit(); conn.close(); return jsonify({"ok": True}), 201
    rows = [dict(r) for r in conn.execute("SELECT * FROM doctor")]
    conn.close(); return jsonify(rows)


@app.route("/api/appointments", methods=["GET", "POST"])
def appointments():
    conn = db()
    if request.method == "POST":
        d = request.get_json() or {}
        # Only blocks an EXACT same-start clash — no 30-min overlap handling.
        clash = conn.execute(
            "SELECT 1 FROM appointment WHERE doctor_id=? AND start_time=? AND status='booked'",
            (d.get("doctor_id"), d.get("start_time")),
        ).fetchone()
        if clash:
            conn.close(); return jsonify({"error": "already booked"}), 400
        conn.execute("INSERT INTO appointment(patient_id,doctor_id,start_time) VALUES(?,?,?)",
                     (d.get("patient_id"), d.get("doctor_id"), d.get("start_time")))
        conn.commit(); conn.close(); return jsonify({"ok": True}), 201
    rows = [dict(r) for r in conn.execute("SELECT * FROM appointment")]
    conn.close(); return jsonify(rows)


if __name__ == "__main__":
    init_db()
    app.run(port=5000)
