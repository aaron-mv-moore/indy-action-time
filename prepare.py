import pandas as pd
from pathlib import Path
from acquire import get_mac_data, get_census_data

def get_clean_mac():
    '''
    This function acquires mac data, renames columns, changes dtypes, fills in null values for the closed date, drops all other null values,
    drops objectid, caseneumber, and source_id, and creates a new columns
    Modules:
        from acquire import get_mac_data
        import pandas as pd
    '''
    df = get_mac_data()

    # change columsn names to lower, remove the __c, and remove 'date'
    col_rename = {}

    for col in df.columns:
        col_rename[col] = col.lower().replace('__c', '').replace('date', '')

    col_rename['LASTMODIFIEDDATE'] = 'last_modified'

    df.rename(col_rename, axis=1, inplace = True)

    # changing multiple columns to date time dtype
    df[['created','last_modified', 'closed']] = df[['created','last_modified', 'closed']].apply(pd.to_datetime)

    # filling in the closeddate nulls with the date the furthest out
    df.closed.fillna(pd.Timestamp.max.floor('30D').tz_localize('US/Eastern'), inplace=True)

    # dropping null values
    print(f'Dropping {df.shape[0] - df.dropna().shape[0]} rows')
    df.dropna(inplace=True)

    # dropping the unneeded columns
    df.drop(['objectid', 'casenumber', 'source_id'], axis=1, inplace=True)

    # adding the time from creation to closing
    df['close_time'] = df['closed'] - df['created']

    # adding the state
    df['state'] = 'IN'
    
    return df

def get_clean_gdf10():
    '''
    This function drops unnecessary columns, edits names, and changes values in 2 columns
    Modules:
        from pathlib import Path
        import pandas as pd
    '''

    # create file path
    data_path = Path('./data')
    file_path = data_path.joinpath('Census_Block_Boundaries_2010_Clean.csv')

    # check for clean data file 
    if file_path.exists():

        # return the clean data
        return pd.read_csv(file_path, index_col=0)
    
    # getting data
    gdf10, gdf20 = get_census_data()

    # drop columns
    cols_to_drop = ['fid', 'uace10', 'uatype', 'statefp10', 'ur10','funcstat10','mtfcc10']
    gdf10.drop(cols_to_drop, axis=1, inplace=True)

    # strip unecesasry values and change feature name
    gdf10.loc[:,'name10'] = gdf10.loc[:,'name10'].str.strip('Block ')
    gdf10.rename({'name10':'blockname10'}, axis=1, inplace=True)

    # lowercase columns and remove extra '_'
    gdf10.columns = gdf10.columns.str.lower().str.replace('__', '_')

    gdf10.to_csv(file_path)
                                          
    return gdf10
    




def get_clean_gdf20():
    '''
    This function drops unnecessary columns, edits names, and changes values in 2 columns
    Modules:
        from pathlib import Path
        import pandas as pd
    '''

    # create file path
    data_path = Path('./data')
    file_path = data_path.joinpath('Census_Block_Boundaries_2020_Clean.csv')

    # check for clean data file 
    if file_path.exists():

        # return the clean data
        return pd.read_csv(file_path, index_col=0)
    
    # getting data
    gdf10, gdf20 = get_census_data()

    # drop columns
    cols_to_drop = ['fid', 'uace20', 'uatype20', 'statefp20', 'ur20','funcstat20','mtfcc20']
    gdf20.drop(cols_to_drop, axis=1, inplace=True)

    # strip unecesasry values and change feature name
    gdf20.loc[:,'name20'] = gdf20.loc[:,'name20'].str.strip('Block ')
    gdf20.rename({'name20':'blockname20'}, axis=1, inplace=True)

    # lowercase columns and remove extra '_'
    gdf20.columns = gdf20.columns.str.lower().str.replace('__', '_')

    gdf20.to_csv(file_path)
                                          
    return gdf20
    