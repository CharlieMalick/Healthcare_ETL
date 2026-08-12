from evals import patient_dict
import pandas as pd

#the main sets are patients, encounters, conditions, medications, immunizations
patients = patient_dict['patients']
encounters = patient_dict['encounters']
conditions = patient_dict['conditions']
medications = patient_dict['medications']
immunizations = patient_dict['immunizations']

#patients: 
#['Id', 'BIRTHDATE', 'DEATHDATE', 'SSN', 'DRIVERS', 'PASSPORT', 'PREFIX', 'FIRST', 'MIDDLE', 'LAST', 'SUFFIX', 'MAIDEN', 
# 'MARITAL','RACE', 'ETHNICITY', 'GENDER', 'BIRTHPLACE', 'ADDRESS', 'CITY', 'STATE', 'COUNTY', 'FIPS', 'ZIP', 
# 'LAT', 'LON', 'HEALTHCARE_EXPENSES', 'HEALTHCARE_COVERAGE', 'INCOME']

#encounters
# ['Id', 'START', 'STOP', 'PATIENT', 'ORGANIZATION', 'PROVIDER', 'PAYER', 'ENCOUNTERCLASS', 'CODE', 'DESCRIPTION', 'BASE_ENCOUNTER_COST', 
# 'TOTAL_CLAIM_COST', 'PAYER_COVERAGE', 'REASONCODE', 'REASONDESCRIPTION']

#conditions
# ['START', 'STOP', 'PATIENT', 'ENCOUNTER', 'SYSTEM', 'CODE', 'DESCRIPTION']

#medications
#['START', 'STOP', 'PATIENT', 'PAYER', 'ENCOUNTER', 'CODE', 'DESCRIPTION', 
# 'BASE_COST', 'PAYER_COVERAGE', 'DISPENSES', 'TOTALCOST', 'REASONCODE', 'REASONDESCRIPTION']

#immunizations
# ['DATE', 'PATIENT', 'ENCOUNTER', 'CODE', 'DESCRIPTION', 'BASE_COST']

#the plan for cleaning is to start with patients, then clean the remainders
#print(patients.isna().sum())
# when cleaning, i noted that EVERY column in suffix was empty and maiden was also 3/4 empty, so i'm dropping them
patients = patients.drop(columns=['SUFFIX', 'MAIDEN', 'PREFIX', 'FIPS'])
patients['IS_DECEASED'] = patients['DEATHDATE'].notna()
patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'])
patients['DEATHDATE'] = pd.to_datetime(patients['DEATHDATE'])

encounters['START'] = pd.to_datetime(encounters['START'])
encounters['STOP'] = pd.to_datetime(encounters['STOP'])

conditions['IS_ACTIVE'] = conditions['STOP'].notna()
conditions['START'] = pd.to_datetime(conditions['START'])
conditions['STOP'] = pd.to_datetime(conditions['STOP'])

medications['IS_ACTIVE'] = medications['STOP'].notna()
medications['START'] = pd.to_datetime(medications['START'])
medications['STOP'] = pd.to_datetime(medications['STOP'])

immunizations['DATE'] = pd.to_datetime(immunizations['DATE'])

print(patients.dtypes)
print(encounters.dtypes)
print(conditions.dtypes)
print(medications.dtypes)
print(immunizations.dtypes)