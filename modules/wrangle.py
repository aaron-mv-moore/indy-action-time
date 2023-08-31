import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# ACQUISITION
#-------------------------------------------------------------------------
def get_mac_data():
    '''
    This function acquires the Mayor Action Center's Service Cases
    Modules required:
        import pandas as pd
    '''
    # read the file
    df = pd.read_csv('./data/Mayor_s_Action_Center_Service_Cases.csv')

    return df

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

# PREPARATION & CLEANING
#-------------------------------------------------------------------------
def clean_mac_col_names(df):
    '''
    This function cleans all the column names for the mac data set
    '''
     # change columsn names to lower, remove the __c, remove date, add a space
    col_rename = {}

    for col in df.columns:
       
        col_rename[col] = col.lower().replace('__c', '').replace('date', '')

    col_rename['LASTMODIFIEDDATE'] = 'last_modified'

    df.rename(col_rename, axis=1, inplace = True)

    return df

#-------------------------------------------------------------------------
def clean_mac_dtypes(df):
    '''
    Change the data type of council district and zip code to string object, change date columns to date time format
    '''   
    # changing dtype to string object
    df['council_district'] = df.council_district.astype(int).astype(str)
    df['zip'] = df.zip.astype(str)

    # changing multiple columns to date time dtype
    df[['created','last_modified', 'closed']] = df[['created','last_modified', 'closed']].apply(pd.to_datetime)

    return df

#-------------------------------------------------------------------------

def drop_mac_cols(df, status_focus):
    '''
    This function drops unnecessary columns
    '''
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
    df.drop(['objectid', 'casenumber', 'source_id', 'incident_address', 'last_modified', 'response_time', 'created', 'closed', 'index', 'city'], axis=1, inplace=True)

    return df

#-------------------------------------------------------------------------

def remove_outliers(df, k=1.5):
    '''
    Actions: removies outliers using the IQR with a default k of 1.5
    '''
    # initialize dictionary
    col_qs = {}
    
    # assign column names to variable
    df_cols = df.columns
    
    # creates a list of column names
    df_cols = df_cols.to_list()
    
    # remove cat cols
    cat_cols = cat_cols = [col for col in df.columns if df[col].dtype == 'O']

    for col in cat_cols:
        df_cols.remove(col)

    # for each column
    for col in df_cols:
        
        # create qualtiles and put them in a dict
        col_qs[col] = q1, q3 = df[col].quantile([0.25, 0.75])

    # for each col
    for col in df_cols:    
        
        # calculate the iqr
        iqr = col_qs[col][0.75] - col_qs[col][0.25]
        
        # calculate the lower fence
        lower_fence = col_qs[col][0.25] - (iqr*k)
        
        # calculates the upper fence
        upper_fence = col_qs[col][0.75] + (iqr*k)
        
        # remove outliers from df for each column
        df = df[(df[col] > lower_fence) & (df[col] < upper_fence)]
        
    # exit df and return new df
    return df

#-------------------------------------------------------------------------

def clean_mac_keywords(df):
    '''
    This function cleans the keywords and some of the subcategories when applicable. 
    '''
    # replacing values
    replace_keyword_values = { 'Debris/Litter' : 'dumping_debris', 'Illegal Dumping' : 'dumping_debris', 'Illegal Dumping and Junk/Trash' : 'dumping_debris' }
    replace_subcategory_values = {'96 Gal Cart': '96 Gal Cart - Other', 'Commercial Veh Storage': 'Commercial Vehicle Storage'}
    df.replace({'keyword' : replace_keyword_values, 'subcategory': replace_subcategory_values}, inplace=True)

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

#-------------------------------------------------------------------------

def get_feature_num_cases(df):
    '''
    This function takes a df and creates a new columns that represents all the open cases at the time of the case creation date.
    '''

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

#-------------------------------------------------------------------------

def get_mac_create_times(df):
    '''
    This function adds four new columns for the month year week and weekday a service request was made
    '''

    # getting the created times
    df['month_created'], df['week_created'] = df.created.dt.month, df.created.dt.isocalendar().week

    return df


#-------------------------------------------------------------------------

def get_clean_mac(status_focus = 'closed'):
    '''
    This function acquires mac data, renames columns, changes dtypes, drops all  null values,
    drops objectid, caseneumber, and source_id, and creates a new columns
    KWARG: status_focus: 'closed' drops all open status cases and the status column
    Modules:
        from acquire import get_mac_data
        import pandas as pd
    '''
    # get data
    df = get_mac_data()

    # change columsn names to lower, remove the __c and that's it
    df = clean_mac_col_names(df)
    
    # dropping null values
    # print(f'Dropping {df.shape[0] - df.dropna().shape[0]} rows')
    df.dropna(inplace=True)

    # change zip, council dtypes and created, closed, last modified dtypes
    df = clean_mac_dtypes(df)

    # adding the time from creation to closing
    df['response_time'] = df['closed'] - df['created']

    # removing outliers
    df = remove_outliers(df, k=3)

    # get new feature
    # sorting the values and reset the index
    df.sort_values(by='created', inplace = True)
    df.reset_index(inplace=True)
    df = get_feature_num_cases(df)

    # get created time features
    df = get_mac_create_times(df)

    # getting new binary target
    df['is_less_than_one_week'] = (df['closed'] - df['created']) <  pd.Timedelta('1W')

    # drop unecessayr columns
    df = drop_mac_cols(df, status_focus=status_focus)
    
    return df


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

# SPLITTING
#-------------------------------------------------------------------------
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
        print('No stratification applied during the split')
        
        # split that data 80/20
        train_validate, test = train_test_split(df, train_size=.8, random_state = 1017)
        
        # splitting train_validate 70/30
        train, validate = train_test_split(train_validate, train_size=.7, random_state=1017)
    
    return train, validate, test

#-------------------------------------------------------------------------

def X_y_split(df, target, stratify = False):
    '''
    This function takes a dataframe and splits it into the X and y train validate and test datasets
    Args:
        df : dataframe
        target : str, the y, or the output variable
        stratify : bool, stratify on the target | default:False
    Returns: train, validate, test,
         X_train,y_train,
             X_validate, y_validate,
                  X_test, y_test 
    Modules:
        from prepare_module import split_data
        import pandas as pd
    '''
    # For stratification
    if stratify == True:

        # split the data witha  stratification on the target specified
        train, validate, test = split_data(df, stratify_on = target)
    
    # otherwise
    else:

        # split with no stratification
        train, validate, test = split_data(df)

    # isolate input and output data for train, validate, and test
    X_train, y_train = train.drop(target, axis=1), train[target]
    X_validate, y_validate = validate.drop(target, axis=1), validate[target]
    X_test, y_test = test.drop(target, axis=1), test[target]

    # print(X_train.shape[0] + y_train.shape[0] == train.shape[0], X_validate.shape[0] + y_validate.shape[0] == validate.shape[0], X_test.shape[0] + y_test.shape[0] == test.shape[0] )
    return train, validate, test,\
         X_train,y_train,\
             X_validate, y_validate,\
                  X_test, y_test 