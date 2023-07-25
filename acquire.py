import pandas as pd

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