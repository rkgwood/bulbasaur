import matplotlib.pyplot
import numpy
import pandas
from scipy import stats

crime_df = pandas.read_csv('data/35019-0004-Data.tsv', sep='\t')
hai_df = pandas.read_csv('data/HAI_map_data/HAI_map_2011-13_data.csv', encoding='ISO-8859-1')
crime_cats = ['MURDER', 'RAPE', 'ROBBERY', 'AGASSLT', 'BURGLRY', 'LARCENY', 'MVTHEFT', 'ARSON']

def construct_fips(row):
    state, county = str(int(row['FIPS_ST'])), str(int(row['FIPS_CTY']))
    if len(state) == 1:
        state = '0' + state
    if len(county) == 1:
        county = '00' + county
    elif len(county) == 2:
        county = '0' + county

    return state + county

def sum_cats(row):
    return sum(map(lambda crime_cat: int(row[crime_cat]), crime_cats))

crime_df['county'] = crime_df.apply(construct_fips, axis=1)

df = pandas.merge(crime_df, hai_df, on='county', how='inner')
df['total_crime'] = df.apply(sum_cats, axis=1)
df['total_crime_per_capita'] = df.apply(lambda x: (x['total_crime'] / x['CPOPARST']) if x['CPOPARST'] else 0, axis=1)


filtered = df[numpy.isfinite(df['per100'])]

slope, intercept, r_value, p_value, std_err = stats.linregress(filtered['per100'], filtered['total_crime_per_capita'])
print("slope: %s, intercept: %s, r_value: %s, p_value: %s, std_err: %s" % (slope, intercept, r_value, p_value, std_err))
matplotlib.pyplot.scatter(filtered['per100'], filtered['total_crime_per_capita'])
matplotlib.pyplot.show()

