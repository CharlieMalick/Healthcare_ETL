from etl.cleaning import patients, encounters, conditions, medications, immunizations
from sqlalchemy import create_engine

def get_engine(user='postgres', password='yourpassword', host='127.0.0.1', port='5433', dbname='healthcare'):
    """Builds and returns a SQLAlchemy engine connected to the Postgres database."""
    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
    return create_engine(connection_string)


def load_table_to_db(df, table_name, engine):
    """Writes a DataFrame to the database as a table, replacing it if it already exists."""
    df.to_sql(table_name, engine, if_exists='replace', index=False)

engine = get_engine()

load_table_to_db(patients, 'patients', engine)
load_table_to_db(encounters, 'encounters', engine)
load_table_to_db(conditions, 'conditions', engine)
load_table_to_db(medications, 'medications', engine)
load_table_to_db(immunizations, 'immunizations', engine)