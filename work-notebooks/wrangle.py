import pandas as pd
from prepare_module import remove_outliers
from pathlib import Path
import requests
from sklearn.model_selection import train_test_split

# AQCUISITION 

def get_census_data():
    '''
    This module acquires the census block identifiers and geometry for the 2020 and 2010 Deciennieal Census 
    Modules:
        import pandas as pd
    '''
    # acquire the data from 2010
    gdf10 = pd.read_csv('../data/Census_Block_Boundaries_2010.csv')

    # acquire the census blocks from 2020
    gdf20 = pd.read_csv('../data/Census_Block_Boundaries_2020.csv')
    
    return gdf10, gdf20


# creating a function to acquire the raw dfata
def get_mac_data():
    '''
    This function acquires the Mayor Action Center's Service Cases
    Modules required:
        import pandas as pd
    '''
    # read the file
    df = pd.read_csv('../data/Mayor_s_Action_Center_Service_Cases.csv')

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

# PREPARATION

def clean_mac_keywords(df):
    '''
    This function cleans the keywords and some of the subcategories when applicable. 
    '''
    # all together
    mask = ['keyword', 'subcategory']

    # Combining 3 keywords into one
    replace_values = { 'Debris/Litter' : 'dumping_debris', 'Illegal Dumping' : 'dumping_debris', 'Illegal Dumping and Junk/Trash' : 'dumping_debris' }
    df.replace({'keyword' : replace_values}, inplace=True)

    # Changing the keyword for a chuckhole
    chuck_street_mask = (df['subcategory'] == 'Street (Chuckhole)') & (df['keyword'] == 'Streets')
    df.loc[chuck_street_mask, 'keyword'] = 'Chuckhole'

    # Changing the keyword for the caveins to chuck holes also
    chuck_street_cave_mask = (df['subcategory'] == 'Cave In')
    df.loc[chuck_street_cave_mask, 'keyword'] = 'Chuckhole'

    # replacing the / in  'Raised/Uneven Surface' to create one subcategory  'Raised Uneven Surface'
    streets_key_mask = df['keyword'] == 'Streets'
    df.loc[streets_key_mask, 'subcategory'] = df.loc[streets_key_mask, 'subcategory'].str.replace('/', ' ')

    # Changing the keyword from 'Alley' to  'dumping_debris'
    brush_debris_mask = df['subcategory'] == 'Brush/Vegetation Removal'
    df.loc[brush_debris_mask, 'keyword'] =  'dumping_debris'
    # changing 'Brush/Vegetation Removal' to 'Debris in Alley/Street' for consistency
    df.loc[brush_debris_mask, 'subcategory'] = 'Debris in Alley/Street'

    # combiningg alley and street keyword into one
    alley_streets_mask = (df['keyword'] == 'Alley') | (df['keyword'] == 'Streets')
    df.loc[alley_streets_mask,'keyword'] = 'streets_alley'
    # adding alley to ruts/grade in case there is noticeable difference
    rg_alley_mask = df['subcategory'] == 'Ruts/Grade'
    df.loc[rg_alley_mask,'subcategory'] = 'Ruts/Grade Alley'

    # replacing the plus signs in the keywords to merge groups
    df['keyword'] = df['keyword'].str.replace('+', ' ')

    # correcting a keyword error Signals to Signs
    request_signs_mask = df['subcategory'] == 'Request (Signs)'
    df.loc[request_signs_mask, 'keyword'] = 'Signs/Traffic Signs'

    return df

def get_feature_num_cases(df):
    '''
    This function takes a df and creates a new columns that represents all the open cases at the time of the case creation date.
    '''
    # sorting the values and reset the index
    df.sort_values(by='created', inplace = True)
    df.reset_index(inplace=True)

    # Create a list with values for num of cases
    res = []
    # create series with closed dates
    temp = df['closed']

    # for each row contents and inde of each row
    for i, row in df.iterrows():
        # get the sum of all the Trues from comparing the creation date to all the close dates 
        # (if close date less than the open date then the older case is closed so false)
        temp_res = np.sum(row['created'] < temp.iloc[:i])
        # add the values in order
        res.append(temp_res)

    # add column with the results
    df['num_open_cases'] = res

    return df

def get_clean_mac(status_focus = 'closed'):
    '''
    This function acquires mac data, renames columns, changes dtypes, fills in null values for the closed date, drops all other null values,
    drops objectid, caseneumber, and source_id, and creates a new columns
    KWARG: status_focus: 'closed' drops all open status cases and the status column
    Modules:
        from acquire import get_mac_data
        import pandas as pd
    '''
    # get data
    df = get_mac_data()

    # change columsn names to lower, remove the __c and that's it
    col_rename = {}

    for col in df.columns:
       
        col_rename[col] = col.lower().replace('__c', '').replace('date', '')

    col_rename['LASTMODIFIEDDATE'] = 'last_modified'

    df.rename(col_rename, axis=1, inplace = True)

    df = clean_mac_keywords(df)

    # changing multiple columns to date time dtype
    df[['created','last_modified', 'closed']] = df[['created','last_modified', 'closed']].apply(pd.to_datetime)

    # dropping null values
    # print(f'Dropping {df.shape[0] - df.dropna().shape[0]} rows')
    df.dropna(inplace=True)

    # KWARG if we only focus on closed status
    if status_focus == 'closed':

        # keep only closed status cases
        df = df[df.status == 'Closed']

        # and drop the status col bc no variance
        df.drop('status', axis=1, inplace=True)    
        
    # KWARG if we want open - keep it the same
    elif status_focus == 'open': 
    
        pass

    # dropping the unneeded columns
    df.drop(['objectid', 'casenumber', 'source_id', 'incident_address', 'last_modified'], axis=1, inplace=True)

    # changing dtype to string object
    df['council_district'] = df.council_district.astype(int).astype(str)
    df['zip'] = df.zip.astype(str)

    # adding the time from creation to closing
    df['response_time'] = df['closed'] - df['created']
    
    # removing outliers
    df = remove_outliers(df, k=3)

    # get new feature
    df = get_feature_num_cases(df)

    # making the reponse times discrete time frames
    df['response_time_frame'] = pd.cut(df['response_time'], 5, labels=['one week', '2 weeks', '3 weeks', '4 weeks','5 weeks'])

    # dropping time related columns
    df.drop(['response_time', 'created', 'closed', 'index'], axis=1, inplace=True)
    
    return df

# def get_clean_gdf10():
#     '''
#     This function drops unnecessary columns, edits names, and changes values in 2 columns
#     Modules:
#         from pathlib import Path
#         import pandas as pd
#     '''

#     # create file path
#     data_path = Path('../data')
#     file_path = data_path.joinpath('Census_Block_Boundaries_2010_Clean.csv')

#     # check for clean data file 
#     if file_path.exists():

#         # return the clean data
#         return pd.read_csv(file_path, index_col=0)
    
#     # getting data
#     gdf10, gdf20 = get_census_data()

#     # drop columns
#     cols_to_drop = ['fid', 'uace10', 'uatype', 'statefp10', 'ur10','funcstat10','mtfcc10']
#     gdf10.drop(cols_to_drop, axis=1, inplace=True)

#     # strip unecesasry values and change feature name
#     gdf10.loc[:,'name10'] = gdf10.loc[:,'name10'].str.strip('Block ')
#     gdf10.rename({'name10':'blockname10'}, axis=1, inplace=True)

#     # lowercase columns and remove extra '_'
#     gdf10.columns = gdf10.columns.str.lower().str.replace('__', '_')

#     gdf10.to_csv(file_path)
                                          
#     return gdf10
    

# def get_clean_gdf20():
#     '''
#     This function drops unnecessary columns, edits names, and changes values in 2 columns
#     Modules:
#         from pathlib import Path
#         import pandas as pd
#     '''

#     # create file path
#     data_path = Path('../data')
#     file_path = data_path.joinpath('Census_Block_Boundaries_2020_Clean.csv')

#     # check for clean data file 
#     if file_path.exists():

#         # return the clean data
#         return pd.read_csv(file_path, index_col=0)
    
#     # getting data
#     gdf10, gdf20 = get_census_data()

#     # drop columns
#     cols_to_drop = ['fid', 'uace20', 'uatype20', 'statefp20', 'ur20','funcstat20','mtfcc20']
#     gdf20.drop(cols_to_drop, axis=1, inplace=True)

#     # strip unecesasry values and change feature name
#     gdf20.loc[:,'name20'] = gdf20.loc[:,'name20'].str.strip('Block ')
#     gdf20.rename({'name20':'blockname20'}, axis=1, inplace=True)

#     # lowercase columns and remove extra '_'
#     gdf20.columns = gdf20.columns.str.lower().str.replace('__', '_')

#     gdf20.to_csv(file_path)
                                          
#     return gdf20
    
# def get_clean_2020_census():
#     '''
#     This function cleans the 2020 Decennial Census Data
#     Modules:
#         get_2020_census_data
#         get_2020_census_labels
#     '''
#     # get and check data
#     df = get_2020_census_data()

#     # getting labels
#     labels = get_2020_census_labels()

#     # drop all columns with nulls
#     df.dropna(axis=1, inplace = True)

#     # getting a list of the column names fromt he labels
#     col_names = list(df.columns.map(labels['label']))

#     # cleaning list
#     cleaned_list = [x for x in col_names if str(x) != 'nan']

#     # adding missing col nmes
#     cleaner_list = cleaned_list + ['state', 'zip']

#     # change col names
#     df.columns = cleaner_list

#     # format col names
#     df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('!!', '_')

#     # rearranging the zip codes
#     df = df.set_index('zip').reset_index()

#     # getting a list of the columns that have less than only one value count
#     ls = []
#     for col in df.columns:
#         if len(df[col].value_counts()) < 5:
#             ls.append(col)
    
#     # drop the columns with only a few value_counts
#     df.drop(ls, axis=1, inplace = True)

#     return df

# WRANGLING

def split_data(df, stratify_on=None):
    '''
    Arguments: prepared dataframe, optional target - must be a string literal that is a column title
    Actions: 
        1. Splits the dataframe with 80% of the data assigned to tv and 20% assigned to test
        2. Splits the tv dataset with 70% of tv assigned to train and 30% assigned to validate
    Returns: 3 variables, each containing a portion
    Modules: from sklearn.model_selection import train_test_split, pandas as pd
    Note: Order matters with variable assignment
    '''
    
    # when the target is a string that is a column title
    if stratify_on in df.columns.to_list():
        # the data is split 80/20 with the target used for stratification
        train_validate, test = train_test_split(df, train_size=.8, random_state = 1017,
                stratify = df[stratify_on])
        
         # splitting train_validate 70/30 with the target used for stratification
        train, validate = train_test_split(train_validate, train_size=.7, stratify=train_validate[stratify_on])
    # for all other targets
    else:
        # inform user that there is no stratification
        # print('No stratification applied during the split')
        
        # split that data 80/20
        train_validate, test = train_test_split(df, train_size=.8, random_state = 1017)
        
        # splitting train_validate 70/30
        train, validate = train_test_split(train_validate, train_size=.7, random_state=1017)
    
    return train, validate, test

def wrangle_data():
    '''
    This function
    Modules:
        import pandas as pd
        from prepare import get_clean_2020_census, get_clean_mac
        from prepare_module import split_data
    '''
    # getting data
    mac = get_clean_mac()
    census = get_clean_2020_census()

    # merge data sets
    df = pd.merge(mac, census, how='left', on='zip' )

    # split data
    train, validate, test = split_data(df)

    return df, train, validate, test