
import os
import pandas as pd
import statsmodels.api as sm
import numpy as np

data_dir = '/Users/marcinic/american_messi/data'

# Merge using city string players to county-level fips code
prospects = pd.read_csv(os.path.join(data_dir,'prospects_v2.csv'))
prospects['city_state'] = prospects['city']+', '+prospects['state']

city_counties = pd.read_csv(os.path.join(data_dir,'USCitiesCountiesv1.csv'))
city_counties['city_state'] = city_counties['City']+', '+city_counties['State full']
del city_counties['City alias']
city_counties = city_counties.drop_duplicates()


merge1 = prospects.merge(city_counties,on='city_state',how='left')
merge1 = merge1[pd.notnull(merge1.County)] # Drop European based players

# Get unique player callups
callups = merge1[~merge1.duplicated(subset=['name'])]
county_players = callups.groupby('County',as_index=False).city.count()
county_players.columns = ['County','num_players']

# Merge players to economic data
census = pd.read_csv(os.path.join(data_dir,'2016CombinedCountyIncomePopulation.csv'))
census['County'] = census.County.str.split().str.get(0).str.upper()
census['income'] = census['Median Household Income'].str.replace('$','').str.replace(',','').astype('float')

data = county_players.merge(census,on='County',how='outer')


# Run regression
model  = sm.OLS(data.num_players,data[['income','Population']])
res = model.fit()
print(res.summary())

#Compute residuals
data['y_pred'] = res.predict()
data['residual'] = data['num_players']-data['y_pred']

# Output final regression dataset
data.to_csv(os.path.join(data_dir,'final_data.csv'))


# Predict model out of sample
X = np.array(census['income','Population'])
census['y_pred'] = model.predict(X)
census.to_csv('out_of_sample_predictions.csv')