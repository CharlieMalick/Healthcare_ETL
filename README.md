# Healthcare ETL Pipeline

A data engineering pipeline that transforms synthetic electronic health record (EHR) data into a validated, queryable relational database — built to mirror the kind of data engineering work done at a hospital or healthcare IT company: ingesting raw data, enforcing data quality before it's trusted, and making it usable for downstream analytics.

## Overview

This project simulates a real-world scenario: a health system needs reliable, validated data before care management or analytics teams can build reports on top of it. The pipeline takes synthetic patient data, cleans and enriches it, validates it against explicit data-quality rules, and loads it into PostgreSQL — with a Tableau dashboard on top demonstrating the value of that trusted data layer.

## Data Source

Patient data is generated using [Synthea](https://github.com/synthetichealth/synthea), an open-source synthetic patient generator that produces realistic (but entirely fake) medical histories — no real patient data is used anywhere in this project.

The generator produced **17 tables** covering demographics, clinical events, and billing:

- **Core clinical tables:** `patients`, `encounters`, `conditions`, `medications`, `immunizations`
- **Supporting tables:** `allergies`, `careplans`, `claims`, `claims_transactions`, `devices`, `imaging_studies`, `observations`, `payer_transitions`, `payers`, `procedures`, `providers`, `supplies`

## Architecture

The pipeline follows a standard ETL structure, with the five core clinical tables receiving full engineering rigor and the twelve supporting tables receiving lighter treatment (see "Core vs. Supporting Tables" below).

```
Synthea (CSV export)
        │
        ▼
   Extract (evals.py)
        │
        ▼
  Transform (cleaning.py)
        │
        ▼
  Validate (validate.py) ── Great Expectations
        │
        ▼
    Load (load.py / light_load.py)
        │
        ▼
   PostgreSQL (Docker)
        │
        ▼
      Tableau
```

### Extract
Loads all 17 generated CSV files into pandas DataFrames.

### Transform
Applied to the five core tables:
- Dropped columns that were empty or administratively irrelevant to clinical analysis (e.g., `SUFFIX`, `MAIDEN`, `FIPS`)
- Converted date fields (`BIRTHDATE`, `DEATHDATE`, `START`, `STOP`) to proper datetime types
- Derived new fields:
  - `IS_DECEASED` — whether a patient has a recorded death date
  - `IS_ACTIVE` — whether a condition or medication is still ongoing (no stop date recorded)
  - `AGE` — computed from birthdate, using death date where applicable
- Verified referential integrity across all core tables (e.g., every `PATIENT` reference in `encounters`, `conditions`, `medications`, and `immunizations` correctly maps back to a real patient)

A key pattern discovered during cleaning: a missing value in a date field (like `STOP` or `DEATHDATE`) usually signals an ongoing or still-alive status — not incomplete data. This distinction shaped both the cleaning decisions and the derived columns above.

### Validate
Uses [Great Expectations](https://greatexpectations.io/) to codify 12 data-quality rules across the five core tables, covering null checks, valid ranges, and required fields:

| Table | Checks |
|---|---|
| `patients` | `Id` not null, `AGE` between 0–120, `BIRTHDATE` not null |
| `encounters` | `Id` not null, `PATIENT` not null, `START` not null |
| `conditions` | `PATIENT` not null, `ENCOUNTER` not null |
| `medications` | `PATIENT` not null, `DISPENSES` greater than 0 |
| `immunizations` | `PATIENT` not null, `CODE` not null |

All 12 checks pass against the current dataset.

### Load
Writes the five validated core tables into PostgreSQL. The twelve supporting tables are loaded separately with lighter validation, to serve as contextual data for the dashboard.

### Test
Core transformation logic was refactored into standalone, reusable functions and covered with a `pytest` suite:
- `calculate_age()` — verified against fixed, known dates
- `add_is_deceased()` — verified against a small constructed dataset
- `add_is_active()` — verified against a small constructed dataset

## Core vs. Supporting Tables

Not all 17 tables received the same level of engineering rigor, and that split was a deliberate scoping decision:

- **Core tables** (`patients`, `encounters`, `conditions`, `medications`, `immunizations`) went through full Extract → Transform → Validate → Load → Test, since they represent the primary clinical entities most relevant to care and outcomes analysis.
- **Supporting tables** (billing, administrative, and lower-priority clinical data) were loaded with lighter validation. They provide useful context for the dashboard but weren't the focus of the data-quality engineering work.

This mirrors a real prioritization decision a data team would make: spend deep validation effort where it matters most, rather than spreading it evenly and thinly across everything.

## Tech Stack

- **Python** / **pandas** — data loading and transformation
- **Great Expectations** — automated data quality validation
- **PostgreSQL** — relational database
- **Docker** — containerized database environment
- **pytest** — unit testing for pipeline logic
- **Tableau** — dashboard and visualization
- **Git / GitHub** — version control

## Project Structure

```
Healthcare-ETL/
├── etl/
│   ├── evals.py           # Extract: loads all 17 CSVs
│   ├── cleaning.py        # Transform: cleans and enriches core 5 tables
│   ├── validate.py        # Validate: Great Expectations checks
│   ├── load.py             # Load: writes core 5 tables to Postgres
│   ├── light_load.py      # Load: writes supporting 12 tables to Postgres
│   └── tests/
│       └── test_cleaning.py
├── synthea/                # Synthea generator (not tracked in git)
└── README.md
```

## Running the Pipeline

1. Start PostgreSQL via Docker:
   ```bash
   docker run --name healthcare-postgres -e POSTGRES_PASSWORD=yourpassword -e POSTGRES_DB=healthcare -p 5433:5432 -d postgres
   ```
2. Generate synthetic data with Synthea (CSV export):
   ```bash
   ./run_synthea -p 100 --exporter.csv.export=true --exporter.fhir.export=false
   ```
3. Run the pipeline, from the project root:
   ```bash
   python3 -m etl.load          # core tables: extract, transform, validate, load
   python3 -m etl.light_load    # supporting tables: extract, load
   ```
4. Run tests:
   ```bash
   python3 -m pytest etl/tests/test_cleaning.py
   ```

## Dashboard

*(Tableau dashboard link and screenshots — coming soon)*

## Notes

This project was built as a portfolio piece to demonstrate healthcare data engineering skills relevant to roles at healthcare IT companies — specifically, the ability to ingest messy real-world-shaped data, enforce data quality before it's trusted, and deliver a usable, tested, documented pipeline rather than a one-off script.
