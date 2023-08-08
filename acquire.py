import pandas as pd
import requests

def get_census_data():
    '''
    This module acquires the census block identifiers and geometry for the 2020 and 2010 Deciennieal Census 
    Modules:
        import pandas as pd
    '''
    # acquire the data from 2010
    gdf10 = pd.read_csv('data/Census_Block_Boundaries_2010.csv')

    # acquire the census blocks from 2020
    gdf20 = pd.read_csv('data/Census_Block_Boundaries_2020.csv')
    
    return gdf10, gdf20



# creating a function to acquire the raw dfata
def get_mac_data():
    '''
    This function acquires the Mayor Action Center's Service Cases
    Modules required:
        import pandas as pd
    '''
    # read the file
    df = pd.read_csv('data/Mayor_s_Action_Center_Service_Cases.csv')

    return df


def get_2020_census_data():
    '''
    This function gets 2020 deciennial data from the census bureau api website for all Zip Code Tabulation Areas (ZCTAs) in the state of Indiana
    Modules:
        import pandas as pd
        import requests
    '''
    # assign url
    url = 'https://api.census.gov/data/2020/dec/dp?get=group(DP1)&for=zip%20code%20tabulation%20area%20(or%20part):*&in=state:18'

    # get data and turn into json
    r = requests.get(url).json()

    # create data frame
    df = pd.DataFrame(r[1:], columns=r[0])

    return df


def get_2020_census_labels():
    '''
    This function pulls that labels associated woith th column names for the 2020 diciennial census data
    '''
    # assign url
    url = 'https://api.census.gov/data/2020/dec/dp/groups/DP1/'

    # get data and turn into json
    r = requests.get(url).json()

    # convert to df
    df = pd.DataFrame(r['variables']).T

    return df