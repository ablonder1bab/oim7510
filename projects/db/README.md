# Babson PT Clinic — Database Design

## The Scenario.

A physical therapy clinic run by Babson alumni currently schedules on a paper
book and keeps paper charts. This database replaces that paper system so the
clinic can book patients without double-booking a therapist, see what each
treatment earns, and find patients it has lost touch with. (Scenario D.)

## The ERD.

```mermaid
erDiagram
    THERAPISTS ||--o{ APPOINTMENTS : treats
    PATIENTS ||--o{ APPOINTMENTS : books
    PATIENTS ||--o{ REFERRALS : has
    APPOINTMENTS ||--o{ APPOINTMENT_TREATMENTS : includes
    TREATMENTS ||--o{ APPOINTMENT_TREATMENTS : "given in"

    THERAPISTS {
        int therapist_id PK
        string first_name
        string last_name
        string credential
        string email
        date hire_date
    }
    PATIENTS {
        int patient_id PK
        string first_name
        string last_name
        date date_of_birth
        string phone
        string email
        string insurance_member_number
    }
    REFERRALS {
        int referral_id PK
        int patient_id FK
        string physician_name
        date referral_date
        string reason
    }
    TREATMENTS {
        int treatment_id PK
        string name
        int standard_minutes
        decimal price
        decimal cost
    }
    APPOINTMENTS {
        int appointment_id PK
        int patient_id FK
        int therapist_id FK
        datetime start_datetime
        int length_minutes
        string status
    }
    APPOINTMENT_TREATMENTS {
        int appointment_id FK
        int treatment_id FK
        decimal price_charged
        int minutes_spent
    }
\`\`\`

## What One Row Means.

*(by hand — one sentence per table, Northwind-style)*

- `therapists`: One row of therapists is one physical therapist or therapy assistant employed by the clinic
- `patients`: One row of patients is one patient registered to receive care at the clinic.
- `referrals`: One row of referrals is one physician’s referral issued for a patient.
- `treatments`: One row of treatments is one specific type of service or procedure offered by the clinic.
- `appointments`: One row of appointments is one scheduled therapy session between a patient and a therapist.
- `appointment_treatments`: One row of appointment_treatments is one specific treatment service delivered to a patient during a single appointment, along with its duration and charge.

## Design Choices.

*(by hand — four short answers, in your own words)*

- Where the business already had a key, such as an email or a ticker, and why: therapists.email — The clinic already assigns unique work email addresses to staff, making it a natural, real-world business identifier rather than an artificial surrogate key. Why we didn't use name or email for patients / why we used patient_id instead: As noted in the prompt, two different patients can share the exact same name and birthday (e.g., family members or common names), so neither name, email, nor combinations of personal details are guaranteed to be unique. A surrogate patient_id ensures every person has a distinct, unambiguous identifier.
- Which relationships are optional, and what in the scenario tells you so: Patients and Referrals (Zero or More): The relationship from patients to referrals is optional because the referrals table carries a required patient_id foreign key referencing patients.patient_id, but a patient can simply have zero rows in that table (which accommodates walk-ins who exist without a physician referral). Patients and Insurance (insurance_member_number): The column is left blank (nullable) because the scenario notes that self-pay patients exist who do not use or have insurance, meaning an insurance identifier is not mandatory.
- Which of the scenario's rules your tables cannot hold, and how you will check it instead: True Schedule Overlaps: While the UNIQUE (therapist_id, start_datetime) constraint prevents two sessions from starting at the exact same minute, it cannot catch overlapping time ranges—such as a 60-minute session starting at 9:00 AM conflicting with another session starting at 9:30 AM. How it gets checked instead: This must be enforced using a query (or validation logic before insert) that checks whether a new proposed start/end time falls within an existing therapist's booked time window (start_datetime to start_datetime + length_minutes). (Alternative options from your list: The as-of-dependent status rule where status changes dynamically based on date, or the rule that total minutes_spent across treatments cannot exceed the overall appointment length).
- One thing your agent proposed that you changed or did not take, and why (or, if you designed it alone, one thing you checked in the ERD your agent drew): Looking closely at the relationship cardinality between patients and referrals, we verified that a patient can have zero or multiple referrals (||--o{), accommodating walk-ins who don't bring a physician referral as well as returning patients who accumulate new referrals over time, rather than forcing a rigid "one-or-more" requirement.