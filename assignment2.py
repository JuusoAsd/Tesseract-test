import requests
import pandas as pd

def main():

    URL = 'https://api-pub.bitfinex.com/v2/conf/pub:map:currency:sym,pub:list:currency:paper,pub:map:currency:label,pub:map:currency:tx:fee'
    r = requests.get(URL)

    a = r.json()

    
    init_df = pd.DataFrame(a[3])
    values = init_df

    values[1] = pd.DataFrame(init_df[1].tolist())[1]
    values.columns = ['Name', 'Fee']
    print(values)


main()