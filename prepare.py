import pandas as pd
from acquire import get_mac_data

def clean_mac_data():
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

    return df