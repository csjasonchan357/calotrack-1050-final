# +
# pip3 install --upgrade google-cloud-bigquery[bqstorage,pandas]
# -

import google.auth
from google.cloud import bigquery
from google.oauth2 import service_account
import expiringdict
import os
#from google.cloud import bigquery_storage_v1beta1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.expanduser('~/.credentials/MyGCPCredentials.json')
client = bigquery.Client()
project_id = 'calotrack-1050-final'
#client = bigquery.Client(credentials= credentials,project=project_id)

RESULT_CACHE_EXPIRATION = 600
_fetch_cache = expiringdict.ExpiringDict(max_len=3, max_age_seconds=RESULT_CACHE_EXPIRATION)


def get_data_cache(allow_cached=False):
    global project_id, client 
    
    def _get_data():
        bquery_job = client.query("""
            SELECT DISTINCT *
            FROM `calotrack-1050-final.nutrition.branded_table`
            WHERE nf_calories != '?'
            """)

        bresults = bquery_job.result()
        bdf = bresults.to_dataframe()
        bdf['serving_unit'].replace('?', 'None', inplace=True)
        bdf['serving_qty'].replace('?', '0', inplace=True)

        cquery_job = client.query("""
        SELECT DISTINCT *
        FROM `calotrack-1050-final.nutrition.common_table`
        WHERE nf_calories != '?'
        """)

        cresults = cquery_job.result()
        cdf = cresults.to_dataframe()
        cdf['serving_unit'].replace('?', 'None', inplace=True)
        cdf['serving_qty'].replace('?', '0', inplace=True)

        equery_job = client.query("""
        SELECT DISTINCT *
        FROM `calotrack-1050-final.nutrition.exercise_table`
        WHERE nf_calories != '?'
        """)

        eresults = equery_job.result()
        edf = eresults.to_dataframe()
        edf = edf[edf['name'] != 'name']
        edf['name'].replace({'hip adduction': 'hip abduction'}, inplace=True)
        
        return bdf, cdf, edf
    
    if allow_cached:
        try:
            return _fetch_cache['cache']
        except KeyError:
            pass
        
    ret = _get_data()
    _fetch_cache['cache'] = ret
    return ret  
    
def get_all_food_data(allow_cached=False):
    df = get_data_cache(allow_cached)
    
    btemp = df[0][['food_name', 'brand_name', 'serving_unit', 'serving_qty', 'nf_calories']]
    ctemp = df[1][['food_name', 'serving_unit', 'serving_qty', 'nf_calories']]
    ctemp['brand_name'] = "None"

    bnew = btemp.rename(columns={'brand_name_item_name': 'food_name'})
    newdf = ctemp.append(bnew, sort=True)
    newdf = newdf[['food_name', 'brand_name', 'serving_unit', 'serving_qty', 'nf_calories']]

    return newdf
