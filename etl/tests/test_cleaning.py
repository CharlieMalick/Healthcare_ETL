import pandas as pd
from etl.cleaning import calculate_age, add_is_deceased, add_is_active

def test_calculate_age_with_fixed_dates():
    birthdate = pd.Timestamp('2000-01-01')
    deathdate = pd.Timestamp('2010-01-01')
    age = calculate_age(birthdate, deathdate)
    assert age == 10

def test_add_is_deceased():
    df = pd.DataFrame({
        'DEATHDATE': [pd.Timestamp('2020-01-01'), pd.NaT, pd.Timestamp('2015-06-15')]
    })
    result = add_is_deceased(df)
    expected = [True, False, True]
    assert list(result['IS_DECEASED']) == expected

def test_add_is_active():
    df = pd.DataFrame({
        'STOP': [pd.Timestamp('2020-01-01'), pd.NaT, pd.Timestamp('2015-06-15')]
    })
    result = add_is_active(df)
    expected = [False, True, False]
    assert list(result['IS_ACTIVE']) == expected