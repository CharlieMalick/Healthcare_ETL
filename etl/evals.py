import pandas as pd

allergies = pd.read_csv('synthea/output/csv/allergies.csv')
careplans = pd.read_csv('synthea/output/csv/careplans.csv')
claims_transactions = pd.read_csv('synthea/output/csv/claims_transactions.csv')
claims = pd.read_csv('synthea/output/csv/claims.csv')
conditions = pd.read_csv('synthea/output/csv/conditions.csv')
devices = pd.read_csv('synthea/output/csv/devices.csv')
encounters = pd.read_csv('synthea/output/csv/encounters.csv')
imaging_studies = pd.read_csv('synthea/output/csv/imaging_studies.csv')
immunizations = pd.read_csv('synthea/output/csv/immunizations.csv')
medications = pd.read_csv('synthea/output/csv/medications.csv')
observations = pd.read_csv('synthea/output/csv/observations.csv')
patients = pd.read_csv('synthea/output/csv/patients.csv')
payer_transitions = pd.read_csv('synthea/output/csv/payer_transitions.csv')
payers = pd.read_csv('synthea/output/csv/payers.csv')
procedures = pd.read_csv('synthea/output/csv/procedures.csv')
providers = pd.read_csv('synthea/output/csv/providers.csv')
supplies = pd.read_csv('synthea/output/csv/supplies.csv')


patient_dict = {"allergies": allergies, "careplans": careplans, "claims_transactions": claims_transactions, "claims": claims, 
                "conditions": conditions, "devices": devices, "encounters": encounters, "imaging_studies": imaging_studies, 
                "immunizations": immunizations, "medications": medications, "observations": observations, 
                "patients": patients, "payer_transitions": payer_transitions, 
                "payers": payers, "procedures": procedures, "providers": providers, "supplies": supplies}

for name, table in patient_dict.items():
    print(name, table.shape)