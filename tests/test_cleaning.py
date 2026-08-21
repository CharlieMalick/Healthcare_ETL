import pandas as pd
from etl.cleaning import calculate_age

def test_calculate_age_with_fixed_dates():
    birthdate = pd.Timestamp('2000-01-01')
    deathdate = pd.Timestamp('2010-01-01')
    age = calculate_age(birthdate, deathdate)
    assert age == 10