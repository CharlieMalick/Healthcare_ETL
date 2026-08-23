from etl.evals import patient_dict
from etl.load import get_engine, load_table_to_db

supporting_tables = ['allergies', 'careplans', 'claims', 'claims_transactions', 'devices',
                      'imaging_studies', 'observations', 'payer_transitions', 'payers',
                      'procedures', 'providers', 'supplies']

engine = get_engine()

for name in supporting_tables:
    df = patient_dict[name]
    load_table_to_db(df, name, engine)