import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl

    return duckdb, mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Tables
    """)
    return


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    database.unlink(missing_ok=True)
    _data_dir = mo.notebook_dir() / "data"

    with duckdb.connect(database) as _con:
        _con.execute("""
            CREATE TABLE therapists (
                therapist_id INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                credential VARCHAR NOT NULL CHECK (credential IN ('DPT', 'PTA')),
                email VARCHAR NOT NULL UNIQUE,
                hire_date DATE NOT NULL
            )
        """)

        _con.execute("""
            CREATE TABLE patients (
                patient_id INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                date_of_birth DATE NOT NULL,
                phone VARCHAR NOT NULL,
                email VARCHAR NOT NULL,
                insurance_member_number VARCHAR
            )
        """)

        _con.execute("""
            CREATE TABLE referrals (
                referral_id INTEGER PRIMARY KEY,
                patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
                physician_name VARCHAR NOT NULL,
                referral_date DATE NOT NULL,
                reason VARCHAR NOT NULL
            )
        """)

        _con.execute("""
            CREATE TABLE treatments (
                treatment_id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL UNIQUE,
                standard_minutes INTEGER NOT NULL,
                price DECIMAL(8,2) NOT NULL CHECK (price > 0),
                cost DECIMAL(8,2) NOT NULL CHECK (cost >= 0)
            )
        """)

        _con.execute("""
            CREATE TABLE appointments (
                appointment_id INTEGER PRIMARY KEY,
                patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
                therapist_id INTEGER NOT NULL REFERENCES therapists(therapist_id),
                start_datetime TIMESTAMP NOT NULL,
                length_minutes INTEGER NOT NULL CHECK (length_minutes IN (30, 45, 60)),
                status VARCHAR NOT NULL CHECK (status IN ('booked', 'completed', 'no-show')),
                UNIQUE (therapist_id, start_datetime)
            )
        """)

        _con.execute("""
            CREATE TABLE appointment_treatments (
                appointment_id INTEGER NOT NULL REFERENCES appointments(appointment_id),
                treatment_id INTEGER NOT NULL REFERENCES treatments(treatment_id),
                price_charged DECIMAL(8,2) NOT NULL CHECK (price_charged > 0),
                minutes_spent INTEGER NOT NULL CHECK (minutes_spent > 0),
                PRIMARY KEY (appointment_id, treatment_id)
            )
        """)

        _therapists_csv = _data_dir / "therapists.csv"
        _patients_csv = _data_dir / "patients.csv"
        _treatments_csv = _data_dir / "treatments.csv"
        _referrals_csv = _data_dir / "referrals.csv"
        _appointments_csv = _data_dir / "appointments.csv"
        _appointment_treatments_csv = _data_dir / "appointment_treatments.csv"

        _con.execute(f"INSERT INTO therapists BY NAME SELECT * FROM read_csv_auto('{_therapists_csv}')")
        _con.execute(f"INSERT INTO patients BY NAME SELECT * FROM read_csv_auto('{_patients_csv}')")
        _con.execute(f"INSERT INTO treatments BY NAME SELECT * FROM read_csv_auto('{_treatments_csv}')")
        _con.execute(f"INSERT INTO referrals BY NAME SELECT * FROM read_csv_auto('{_referrals_csv}')")
        _con.execute(f"INSERT INTO appointments BY NAME SELECT * FROM read_csv_auto('{_appointments_csv}')")
        _con.execute(f"INSERT INTO appointment_treatments BY NAME SELECT * FROM read_csv_auto('{_appointment_treatments_csv}')")

        _con.execute("""
            CREATE VIEW appointment_revenue AS
            SELECT
                appointments.appointment_id,
                appointments.therapist_id,
                appointments.patient_id,
                appointments.start_datetime,
                appointments.status,
                COALESCE(SUM(appointment_treatments.price_charged), 0) AS total_charged,
                COALESCE(SUM(appointment_treatments.minutes_spent), 0) AS total_minutes_spent
            FROM appointments
            LEFT JOIN appointment_treatments
                ON appointments.appointment_id = appointment_treatments.appointment_id
            GROUP BY appointments.appointment_id, appointments.therapist_id, appointments.patient_id,
                     appointments.start_datetime, appointments.status
        """)
    return ask, database


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. The Data

    Generated by `make_data.py`, which writes CSVs into `data/` from a fixed
    random seed. It deliberately breaks the "treatments can't exceed the
    appointment's length" rule in exactly two appointments (appointment_id 1 and
    2), and deliberately includes 20 patients who were referred but never
    booked, and two treatments that are never given.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. A Look at the Data
    """)
    return


@app.cell
def _(mo, pl):
    import altair as alt

    appointment_data = pl.read_csv(mo.notebook_dir() / "data" / "appointments.csv")
    appointments_by_hour = (
        appointment_data
        .with_columns(pl.col("start_datetime").str.to_datetime().dt.hour().alias("hour"))
        .group_by("hour")
        .agg(pl.len().alias("appointment_count"))
        .sort("hour")
    )
    appointments_by_hour_chart = mo.ui.altair_chart(
        alt.Chart(appointments_by_hour.to_pandas()).mark_bar().encode(
            x=alt.X("hour:O", title="Hour of day"),
            y=alt.Y("appointment_count:Q", title="Appointments"),
        ).properties(title="Appointments by hour of day")
    )
    appointments_by_hour_chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Row Counts
    """)
    return


@app.cell
def _(ask):
    row_counts = ask("""
        SELECT 'therapists' AS table_name, COUNT(*) AS row_count FROM therapists
        UNION ALL SELECT 'patients', COUNT(*) FROM patients
        UNION ALL SELECT 'referrals', COUNT(*) FROM referrals
        UNION ALL SELECT 'treatments', COUNT(*) FROM treatments
        UNION ALL SELECT 'appointments', COUNT(*) FROM appointments
        UNION ALL SELECT 'appointment_treatments', COUNT(*) FROM appointment_treatments
    """)
    row_counts
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. A Row It Refuses
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.execute("""
                INSERT INTO appointments (appointment_id, patient_id, therapist_id,
                                           start_datetime, length_minutes, status)
                VALUES (999999, 1, 1, '2026-11-09 09:00:00', 40, 'booked')
            """)
        refused_row_result = "that insert was accepted (unexpected — look into this)"
    except duckdb.ConstraintException as _error:
        refused_row_result = str(_error)

    refused_row_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Answers You Already Knew
    """)
    return


@app.cell
def _(ask):
    known_patient_count = ask("SELECT COUNT(*) AS patient_count FROM patients")  # expect 300
    known_therapist_count = ask("SELECT COUNT(*) AS therapist_count FROM therapists")  # expect 6
    known_never_given_treatments = ask("""
        SELECT treatments.name
        FROM treatments
        LEFT JOIN appointment_treatments
            ON treatments.treatment_id = appointment_treatments.treatment_id
        WHERE appointment_treatments.treatment_id IS NULL
    """)  # expect Post-Surgical Rehab and Sports Injury Rehab
    known_never_given_treatments
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. A View
    """)
    return


@app.cell
def _(ask):
    ask("SELECT * FROM appointment_revenue ORDER BY start_datetime DESC LIMIT 10")
    return


if __name__ == "__main__":
    app.run()
