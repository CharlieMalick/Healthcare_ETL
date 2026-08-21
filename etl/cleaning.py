from etl.evals import patient_dict
import pandas as pd

patients = patient_dict['patients']
encounters = patient_dict['encounters']
conditions = patient_dict['conditions']
medications = patient_dict['medications']
immunizations = patient_dict['immunizations']

def calculate_age(birthdate, deathdate=None):
    reference_date = deathdate if pd.notna(deathdate) else pd.Timestamp.now()
    age = (reference_date - birthdate).days / 365.25
    return round(age)


def add_is_deceased(df, deathdate_column='DEATHDATE'):
    df['IS_DECEASED'] = df[deathdate_column].notna()
    return df


def add_is_active(df, stop_column='STOP'):
    df['IS_ACTIVE'] = df[stop_column].isna()
    return df

patients = patients.drop(columns=['SUFFIX', 'MAIDEN', 'PREFIX', 'FIPS'])
patients = add_is_deceased(patients)
patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'])
patients['DEATHDATE'] = pd.to_datetime(patients['DEATHDATE'])
patients['AGE'] = patients.apply(lambda row: calculate_age(row['BIRTHDATE'], row['DEATHDATE']), axis=1)

encounters['START'] = pd.to_datetime(encounters['START'])
encounters['STOP'] = pd.to_datetime(encounters['STOP'])

conditions = add_is_active(conditions)
conditions['START'] = pd.to_datetime(conditions['START'])
conditions['STOP'] = pd.to_datetime(conditions['STOP'])

medications = add_is_active(medications)
medications['START'] = pd.to_datetime(medications['START'])
medications['STOP'] = pd.to_datetime(medications['STOP'])

immunizations['DATE'] = pd.to_datetime(immunizations['DATE'])

print(patients.columns)
print(patients['AGE'])