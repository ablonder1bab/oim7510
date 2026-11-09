
"""
make_data.py — generates synthetic CSV data for the Babson PT Clinic database.
 
Run with:  uv run python projects/db/make_data.py
 
Writes one CSV per table into projects/db/data/:
  therapists.csv, patients.csv, referrals.csv, treatments.csv,
  appointments.csv, appointment_treatments.csv
"""
 
import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path
 
random.seed(42)
 
AS_OF = date(2026, 11, 8)
START_DATE = AS_OF - timedelta(days=365)
FUTURE_END_DATE = AS_OF + timedelta(days=21)
 
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
 
FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
               "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
               "Thomas", "Sarah", "Charles", "Karen", "Daniel", "Nancy", "Matthew", "Lisa",
               "Anthony", "Betty", "Mark", "Margaret", "Paul", "Sandra", "Steven", "Ashley",
               "Andrew", "Kimberly", "Kenneth", "Emily", "George", "Donna", "Joshua", "Michelle"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
              "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
              "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
              "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
              "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"]
 
 
def random_name():
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)
 
 
def random_date(start, end):
    span = (end - start).days
    return start + timedelta(days=random.randint(0, span))
 
 
def random_weekday_date(start, end):
    while True:
        candidate = random_date(start, end)
        if candidate.weekday() < 5:
            return candidate
 
 
def random_phone():
    return f"617-555-{random.randint(1000, 9999)}"
 
 
# ---------------------------------------------------------------- therapists
CREDENTIALS = ["DPT", "DPT", "DPT", "PTA", "PTA", "DPT"]
therapists = []
for i in range(1, 7):
    first, last = random_name()
    therapists.append({
        "therapist_id": i,
        "first_name": first,
        "last_name": last,
        "credential": CREDENTIALS[i - 1],
        "email": f"{first.lower()}.{last.lower()}@babsonptclinic.com",
        "hire_date": random_date(date(2018, 1, 1), date(2025, 1, 1)).isoformat(),
    })
 
# ------------------------------------------------------------------ patients
PATIENT_COUNT = 300
REFERRED_NEVER_BOOKED_COUNT = 20
 
patients = []
for i in range(1, PATIENT_COUNT + 1):
    first, last = random_name()
    self_pay = random.random() < 0.2
    patients.append({
        "patient_id": i,
        "first_name": first,
        "last_name": last,
        "date_of_birth": random_date(date(1940, 1, 1), date(2010, 1, 1)).isoformat(),
        "phone": random_phone(),
        "email": f"{first.lower()}.{last.lower()}{i}@example.com",
        "insurance_member_number": "" if self_pay else f"INS{random.randint(100000, 999999)}",
    })
 
all_patient_ids = [p["patient_id"] for p in patients]
referred_never_booked_ids = set(random.sample(all_patient_ids, REFERRED_NEVER_BOOKED_COUNT))
bookable_patient_ids = [pid for pid in all_patient_ids if pid not in referred_never_booked_ids]
 
# ----------------------------------------------------------------- referrals
PHYSICIANS = ["Dr. Alan Kessler", "Dr. Nina Park", "Dr. Omar Haddad", "Dr. Rachel Stein",
              "Dr. Victor Diaz", "Dr. Grace Liu", "Dr. Samuel Oduya", "Dr. Teresa Novak"]
REASONS = ["Lower back pain", "Post-surgical knee rehab", "Rotator cuff strain",
           "Ankle sprain recovery", "Chronic neck pain", "Hip replacement follow-up",
           "Sports injury", "Balance and fall risk"]
 
referrals = []
referral_id = 1
# every "referred, never booked" patient gets exactly one referral
for pid in referred_never_booked_ids:
    referrals.append({
        "referral_id": referral_id,
        "patient_id": pid,
        "physician_name": random.choice(PHYSICIANS),
        "referral_date": random_date(START_DATE, AS_OF).isoformat(),
        "reason": random.choice(REASONS),
    })
    referral_id += 1
# about a third of the bookable patients also have a referral on file
for pid in random.sample(bookable_patient_ids, len(bookable_patient_ids) // 3):
    referrals.append({
        "referral_id": referral_id,
        "patient_id": pid,
        "physician_name": random.choice(PHYSICIANS),
        "referral_date": random_date(START_DATE, AS_OF).isoformat(),
        "reason": random.choice(REASONS),
    })
    referral_id += 1
 
# ---------------------------------------------------------------- treatments
treatments = [
    {"treatment_id": 1, "name": "Manual Therapy", "standard_minutes": 30, "price": 65.00, "cost": 20.00},
    {"treatment_id": 2, "name": "Therapeutic Exercise", "standard_minutes": 30, "price": 60.00, "cost": 15.00},
    {"treatment_id": 3, "name": "Ultrasound Therapy", "standard_minutes": 15, "price": 40.00, "cost": 10.00},
    {"treatment_id": 4, "name": "Gait Training", "standard_minutes": 30, "price": 55.00, "cost": 18.00},
    {"treatment_id": 5, "name": "Balance Training", "standard_minutes": 30, "price": 55.00, "cost": 18.00},
    {"treatment_id": 6, "name": "Electrical Stimulation", "standard_minutes": 15, "price": 35.00, "cost": 8.00},
    {"treatment_id": 7, "name": "Hot/Cold Pack Therapy", "standard_minutes": 15, "price": 20.00, "cost": 5.00},
    {"treatment_id": 8, "name": "Dry Needling", "standard_minutes": 20, "price": 75.00, "cost": 25.00},
    {"treatment_id": 9, "name": "Post-Surgical Rehab", "standard_minutes": 45, "price": 90.00, "cost": 30.00},
    {"treatment_id": 10, "name": "Sports Injury Rehab", "standard_minutes": 45, "price": 85.00, "cost": 28.00},
]
NEVER_GIVEN_TREATMENT_IDS = {9, 10}
GIVABLE_TREATMENT_IDS = [t["treatment_id"] for t in treatments if t["treatment_id"] not in NEVER_GIVEN_TREATMENT_IDS]
TREATMENT_BY_ID = {t["treatment_id"]: t for t in treatments}
 
# ------------------------------------------------------------- appointments
APPOINTMENT_COUNT = 3200
FUTURE_COUNT = 400
PAST_COUNT = APPOINTMENT_COUNT - FUTURE_COUNT
LENGTHS = [30, 45, 60]
HOURS = list(range(8, 17))
MINUTES = [0, 15, 30, 45]
 
used_slots = set()
 
 
def free_slot(therapist_id, day):
    while True:
        start = datetime(day.year, day.month, day.day,
                          random.choice(HOURS), random.choice(MINUTES))
        key = (therapist_id, start)
        if key not in used_slots:
            used_slots.add(key)
            return start
 
 
appointments = []
appointment_id = 1
for _ in range(PAST_COUNT):
    patient_id = random.choice(bookable_patient_ids)
    therapist_id = random.choice([t["therapist_id"] for t in therapists])
    day = random_weekday_date(START_DATE, AS_OF)
    start = free_slot(therapist_id, day)
    status = "no-show" if random.random() < 0.15 else "completed"
    appointments.append({
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "therapist_id": therapist_id,
        "start_datetime": start.isoformat(sep=" "),
        "length_minutes": random.choice(LENGTHS),
        "status": status,
    })
    appointment_id += 1
 
for _ in range(FUTURE_COUNT):
    patient_id = random.choice(bookable_patient_ids)
    therapist_id = random.choice([t["therapist_id"] for t in therapists])
    day = random_weekday_date(AS_OF + timedelta(days=1), FUTURE_END_DATE)
    start = free_slot(therapist_id, day)
    appointments.append({
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "therapist_id": therapist_id,
        "start_datetime": start.isoformat(sep=" "),
        "length_minutes": random.choice(LENGTHS),
        "status": "booked",
    })
    appointment_id += 1
 
completed_appointments = [a for a in appointments if a["status"] == "completed"]
 
# ----------------------------------------------------- appointment_treatments
appointment_treatments = []
for appt in completed_appointments:
    treatment_ids = random.sample(GIVABLE_TREATMENT_IDS, random.randint(1, 3))
    for tid in treatment_ids:
        treatment = TREATMENT_BY_ID[tid]
        appointment_treatments.append({
            "appointment_id": appt["appointment_id"],
            "treatment_id": tid,
            "price_charged": round(treatment["price"] * random.uniform(0.95, 1.05), 2),
            "minutes_spent": treatment["standard_minutes"],
        })
 
# break the rule on purpose in exactly two rows: minutes spent on a completed
# appointment exceed the appointment's own length_minutes
BROKEN_RULE_APPOINTMENT_IDS = [completed_appointments[0]["appointment_id"],
                                completed_appointments[1]["appointment_id"]]
broken_log = []
for appt_id in BROKEN_RULE_APPOINTMENT_IDS:
    appt = next(a for a in appointments if a["appointment_id"] == appt_id)
    appt["length_minutes"] = 30
    rows = [row for row in appointment_treatments if row["appointment_id"] == appt_id]
    for row in rows:
        row["minutes_spent"] = 25
    used_treatment_ids = [r["treatment_id"] for r in rows]
    appointment_treatments.append({
        "appointment_id": appt_id,
        "treatment_id": random.choice([tid for tid in GIVABLE_TREATMENT_IDS if tid not in used_treatment_ids]),
        "price_charged": 45.00,
        "minutes_spent": 25,
    })
    total_minutes = sum(row["minutes_spent"] for row in appointment_treatments if row["appointment_id"] == appt_id)
    broken_log.append((appt_id, total_minutes, appt["length_minutes"]))
 
print("Rows that break 'treatments given cannot exceed the appointment length':")
for appt_id, total_minutes, length in broken_log:
    print(f"  appointment_id={appt_id}: {total_minutes} minutes of treatment charged against a {length}-minute appointment")
 
print(f"Treatments never given: {[TREATMENT_BY_ID[tid]['name'] for tid in NEVER_GIVEN_TREATMENT_IDS]}")
print(f"Patients referred but never booked: {len(referred_never_booked_ids)}")
 
 
# --------------------------------------------------------------------- write
def write_csv(filename, rows, fieldnames):
    path = DATA_DIR / filename
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {path}")
 
 
write_csv("therapists.csv", therapists,
          ["therapist_id", "first_name", "last_name", "credential", "email", "hire_date"])
write_csv("patients.csv", patients,
          ["patient_id", "first_name", "last_name", "date_of_birth", "phone", "email", "insurance_member_number"])
write_csv("referrals.csv", referrals,
          ["referral_id", "patient_id", "physician_name", "referral_date", "reason"])
write_csv("treatments.csv", treatments,
          ["treatment_id", "name", "standard_minutes", "price", "cost"])
write_csv("appointments.csv", appointments,
          ["appointment_id", "patient_id", "therapist_id", "start_datetime", "length_minutes", "status"])
write_csv("appointment_treatments.csv", appointment_treatments,
          ["appointment_id", "treatment_id", "price_charged", "minutes_spent"])