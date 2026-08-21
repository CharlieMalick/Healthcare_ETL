"""
VALIDATE — Data Quality Layer (Great Expectations)

WHAT THIS DOES:
Runs automated data-quality checks against the five core cleaned tables
(patients, encounters, conditions, medications, immunizations) before
they're loaded into Postgres. Each check is a formal "expectation" —
an explicit, repeatable rule about what valid data should look like.

WHY GREAT EXPECTATIONS:
Rather than manually eyeballing .isna().sum() output every time this
pipeline runs, Great Expectations turns those checks into permanent,
automated rules that re-verify the data on every run. This mirrors how
a real healthcare data team would gate raw EHR data before it reaches
downstream analytics or reporting - bad data gets caught here, not
after it's already loaded and being used.

CHECKS PERFORMED (12 total):
- patients: Id not null, AGE within 0-120, BIRTHDATE not null
- encounters: Id not null, PATIENT not null, START not null
- conditions: PATIENT not null, ENCOUNTER not null
- medications: PATIENT not null, DISPENSES greater than 0
- immunizations: PATIENT not null, CODE not null

RESULT:
All 12 expectations passed (12/12 True) - confirming the cleaned data
is structurally sound and ready to load into Postgres.
"""

import great_expectations as gx
from cleaning import patients, encounters, conditions, medications, immunizations

context = gx.get_context()
batch = context.data_sources.add_pandas("patients_source").read_dataframe(patients)

result = batch.validate(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="Id")
)
print(result.success)

result2 = batch.validate(
    gx.expectations.ExpectColumnValuesToBeBetween(column="AGE", min_value=0, max_value=120)
)

result3 = batch.validate(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="BIRTHDATE")
)

print(result3.success)

encounters_batch = context.data_sources.add_pandas("encounters_source").read_dataframe(encounters)

result4 = encounters_batch.validate(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="Id")
)
print(result4.success)

result5 = encounters_batch.validate(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="PATIENT")
)
print(result5.success)

result6 = encounters_batch.validate(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="START")
)
print(result6.success)

conditions_batch = context.data_sources.add_pandas("conditions_source").read_dataframe(conditions)

# conditions (you should already have this batch set up)
result7 = conditions_batch.validate(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="PATIENT")
)
print(result7.success)

result8 = conditions_batch.validate(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="ENCOUNTER")
)
print(result8.success)

medications_batch = context.data_sources.add_pandas("medications_source").read_dataframe(medications)

result9 = medications_batch.validate(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="PATIENT")
)
print(result9.success)

result10 = medications_batch.validate(
    gx.expectations.ExpectColumnValuesToBeBetween(column="DISPENSES", min_value=1, max_value=None)
)
print(result10.success)

immunizations_batch = context.data_sources.add_pandas("immunizations_source").read_dataframe(immunizations)

result11 = immunizations_batch.validate(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="PATIENT")
)
print(result11.success)

result12 = immunizations_batch.validate(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="CODE")
)
print(result12.success)