import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

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
        train, validate = train_test_split(train_validate, train_size=.7)
    
    return train, validate, test


def prepare_split(df, base_explore=True):
    '''
    Arguments: cleaned df, base_explore retains variables in a non-encoded format, useful for visualizations and exploration
    Actions:
        1. Creates a dataframe with only dummy variables, numerical variables, and the target
        2. Formats all the column titles for python usability
        3. Splits data into train validate, and test with straitification on target
    Return: train, validate, test
    Modules: pandas as pd
    '''
    # assigning a target
    target = 'ADD TARGET'
    
    # default argument fo base_explore is True
    if base_explore == True:

        # skip the encoding of the variables
        pass
    
    else:
        # Create list of object type/categorical columns
        df_objects = [col for col in df if df[col].dtype == 'O' and col != target]
        
        # Create dummy variables and add them to the df
        df = pd.concat([df, pd.get_dummies(df[df_objects], drop_first=True)], axis=1)
    
        # Create a list of all non-object variables and including the target
        num_cols = [col for col in df if df[col].dtype != 'O' or col == target]

        # creating a df with only the variables needed for exploring and modeling
        df = df[num_cols]

        # change the titles of the encoded variables to be python friendly
        df.columns = df.columns.str.lower().str.strip().str.replace(' ','_')
    
    # edit target series to reflect 1,0 for values
    df[target].replace(['ADD VALUE', 'ADD VALUE'], [1, 0], inplace=True)
    
    # splits the df into train, validate, and test with a stratification on the target
    train, validate, test = split_data(df, stratify_on=target)
    
    return train, validate, test


def nulls_by_row(df):
    '''
    This function takes in a dataframe 
    and finds the number of missing values in a row
    it returns a new dataframe with quantity and percent of missing values
    '''
    # adds all the nulls for each row and assigns it to a variable
    num_missing = df.isnull().sum(axis=1)
    
    # divides the total nulls missing by the number of features; this is mulitplied by 100 to get the percent of rows missing
    percent_miss = num_missing / df.shape[1] * 100
    
    # create a dataframe with both variables from above and assigns to a variable
    rows_missing = pd.DataFrame({'num_cols_missing': num_missing, 'percent_cols_missing': percent_miss})
    
    
    rows_missing = df.merge(rows_missing,
                        left_index=True,
                        right_index=True)[['num_cols_missing', 'percent_cols_missing']]
    
    # returns the dataframe with the largest numbers first
    return rows_missing.sort_values(by='num_cols_missing', ascending=False)


def nulls_by_col(df):
    '''
    This function takes in a dataframe 
    and finds the number of missing values
    it returns a new dataframe with quantity and percent of missing values
    '''
    # adds all the nulls for each row and assigns it to a variable
    num_missing = df.isnull().sum()
    
    # assigne the number of rows to a variable
    rows = df.shape[0]
    
    # calculates the percentage of the column that's missing
    percent_missing = num_missing / rows * 100
    
    # creates a dataframe using the actual number ofmissing values and the percetage of the column that is missing
    cols_missing = pd.DataFrame({'num_rows_missing': num_missing, 'percent_rows_missing': percent_missing})
    
    # returns the dataframe with the largest numbers first
    return cols_missing.sort_values(by='num_rows_missing', ascending=False)


def summarize(df):
    '''
    summarize will take in a single argument (a pandas dataframe) 
    and output to console various statistics on said dataframe, including:
    # .head()
    # .info()
    # .describe()
    # .value_counts()
    # observation of nulls in the dataframe
    '''
    print('                    SUMMARY REPORT')
    print('=====================================================\n\n')
    print('Dataframe head: ')
    display(pd.DataFrame(df.head(3)))
    print('=====================================================\n\n')
    print('Dataframe info: ')
    display(pd.DataFrame(df.info()))
    print('=====================================================\n\n')
    print('Dataframe Description: ')
    display(pd.DataFrame(df.describe().T))
    num_cols = [col for col in df.columns if df[col].dtype != 'O']
    cat_cols = [col for col in df.columns if col not in num_cols]
    print('=====================================================')
    print('DataFrame value counts: ')
    for col in df.columns:
        if col in cat_cols:
            display(pd.DataFrame(df[col].value_counts()))
        else:
            display(pd.DataFrame(df[col].value_counts(bins=10, sort=False)))
    print('=====================================================')
    print('nulls in dataframe by column: ')
    display(pd.DataFrame(nulls_by_col(df)))
    print('=====================================================')
    print('nulls in dataframe by row: ')
    display(pd.DataFrame(nulls_by_row(df)))
    print('=====================================================')


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
    df_cols.remove('red_or_white')

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
        
        # remove outliers from df for each col
        df = df[(df[col] > lower_fence) & (df[col] < upper_fence)]
        
    # exit df and return new df
    return df
