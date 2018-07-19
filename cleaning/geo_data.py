import os
import json
import pandas as pd

data_dir = '/Users/marcinic/american_messi/data'

data = pd.read_csv(os.path.join(data_dir,'final_data.csv'))
data['fips_code'] = data['County Fips'].astype(str)
data['County'] = data['County_x']
data_set = data[['County','fips_code','income','Population','state','num_players','y_pred','residual']]
data_set.loc[data_set.fips_code.str.len()==4,'fips_code'] = '0'+data_set.fips_code

county_lines = os.path.join(data_dir,'cb_2017_us_county_20m.json')


with open(county_lines,'r') as f:
    geojson = json.load(f)
    for feature in geojson['features']:
        feature_properties = feature['properties']
        fips = feature_properties['STATEFP']+feature_properties['COUNTYFP']
        row  = data_set[data_set.fips_code==fips]
        if not row.empty:
            for key in row.columns:
                feature_properties[key] = row[key].item()

out_file = os.path.join(data_dir,'county_performance.json')
with open(out_file,'w') as f:
    json.dump(geojson,f)

