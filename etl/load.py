from cleaning import patients, encounters, conditions, medications, immunizations
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:yourpassword@127.0.0.1:5433/healthcare')

patients.to_sql('patients', engine, if_exists='replace', index=False)
encounters.to_sql('encounters', engine, if_exists='replace', index=False)
conditions.to_sql('conditions', engine, if_exists='replace', index=False)
medications.to_sql('medications', engine, if_exists='replace', index=False)
immunizations.to_sql('immunizations', engine, if_exists='replace', index=False)