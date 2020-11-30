'''
#before you run this script make sure that you execute the SQL script
# Create_tables_database_netflix.sql
#to create the tables in your mySQL database

CHANGE the path for the 2 files
'''


import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy as sqlalchemy

#variable for path of the files
path_netflix_csv = "C:/Users/nikol/OneDrive/Dokumente/Studium/TU Chemnitz/Auslandssemester/Korea/Kurse/Database Management 2/project/netflix_titles.csv"
path_rating_description = "C:/Users/nikol/OneDrive/Dokumente/Studium/TU Chemnitz/Auslandssemester/Korea/Kurse/Database Management 2/project/Ratings-Descriptions.csv"

# Credentials to database connection
hostname = "localhost"
uname = "root"
pwd = "1fcn"
dbname = "dbm_netflix_project"

# Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=hostname, db=dbname, user=uname, pw=pwd))

#=====================FUNCTION TO SPLIT AFTER COMMA ==================================
def tidy_split(df, column, sep='|', keep=False):
    """
    Split the values of a column and expand so the new DataFrame has one split
    value per row. Filters rows where the column is missing.

    Params
    ------
    df : pandas.DataFrame
        dataframe with the column to split and expand
    column : str
        the column to split and expand
    sep : str
        the string used to split the column's values
    keep : bool
        whether to retain the presplit value as it's own row

    Returns
    -------
    pandas.DataFrame
        Returns a dataframe with the same columns as `df`.
    """
    indexes = list()
    new_values = list()
    df = df.dropna(subset=[column])
    for i, presplit in enumerate(df[column].astype(str)):
        values = presplit.split(sep)
        if keep and len(values) > 1:
            indexes.append(i)
            new_values.append(presplit)
        for value in values:
            indexes.append(i)
            new_values.append(value)
    new_df = df.iloc[indexes, :].copy()
    new_df[column] = new_values
    return new_df

#==================FUNCTIONS TO CLEAN DATA AND CREATE TABLES===========================
def CreateShowsTable():
    new_df = df [['show_id', 'type', 'title', 'date_added', 'release_year', 'rating', 'duration', 'season_count', 'description']]
    df_unique = new_df.rename(columns={'rating': 'rating_code'})

    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                           .format(host=hostname, db=dbname, user=uname, pw=pwd))
    try:
        # Convert dataframe to sql table
        df_unique.to_sql('shows', engine, if_exists='append', index=False)
        print("Data sucessfully inserted into table movies")
    except sqlalchemy.exc.IntegrityError:
        print('DatabaseDuplicate key entry error- the data exists already in the database')

def cleanListedIn():
    df_new = df[['listed_in']]
    new_df = tidy_split(df_new, 'listed_in', sep=',')
    #remove leading and trailing space of the column to remove duplicates
    new_df = new_df['listed_in'].str.strip()
    #remove duplicates
    df_unique = new_df.drop_duplicates()
    df_unique=df_unique.to_frame()
    #order df alphabetically
    df_unique = df_unique.sort_values('listed_in')
    #drop old index
    df_unique = df_unique.reset_index(drop=True)
    #add index column
    df_unique['genre_id'] = range(1, len(df_unique) + 1)
    #change order columns
    df_unique = df_unique[['genre_id', 'listed_in']]
    #rename column
    df_unique = df_unique.rename(columns={'listed_in' : 'genre'})

    return df_unique

def createGenreTable():
    df_genre = cleanListedIn()
    try:
        # Convert dataframe to sql table
        df_genre.to_sql('genre', engine, if_exists='append', index=False)
        print("Data sucessfully inserted into table genre")
    except sqlalchemy.exc.IntegrityError:
        print('DatabaseDuplicate key entry error- the data exists already in the database')

def cleanCast():
    df_new = df[['cast']]
    new_df = tidy_split(df_new, 'cast', sep=',')
    #remove leading and trailing space of the column to remove duplicates
    new_df = new_df['cast'].str.strip()
    #print(new_df)
    #remove duplicates
    df_unique = new_df.drop_duplicates()
    df_unique=df_unique.to_frame()
    #order df alphabetically
    df_unique = df_unique.sort_values('cast')
    #drop old index
    df_unique = df_unique.reset_index(drop=True)
    #add index column
    df_unique['actor_id'] = range(1, len(df_unique) + 1)
    #change order columns
    df_unique = df_unique[['actor_id', 'cast']]
    #rename column
    df_unique = df_unique.rename(columns={'cast' : 'actor'})
    return df_unique

def createCast():
    df_unique = cleanCast()
    try:
        # Convert dataframe to sql table
        df_unique.to_sql('actor', engine, if_exists='append', index=False)
        print("Data sucessfully inserted into table actor")
    except sqlalchemy.exc.IntegrityError:
        print('DatabaseDuplicate key entry error- the data exists already in the database')

def cleanDirector():
    df_new = df[['director']]
    new_df = tidy_split(df_new, 'director', sep=',')
    #remove leading and trailing space of the column to remove duplicates
    new_df = new_df['director'].str.strip()
    #remove duplicates
    df_unique = new_df.drop_duplicates()
    df_unique=df_unique.to_frame()
    #order df alphabetically
    df_unique = df_unique.sort_values('director')
    #drop old index
    df_unique = df_unique.reset_index(drop=True)
    #add index column
    df_unique['director_id'] = range(1, len(df_unique) + 1)
    #change order columns
    df_unique = df_unique[['director_id', 'director']]

    return (df_unique)

def createTableDirector():
    df_diretor = cleanDirector()
    try:
        # Convert dataframe to sql table
        df_diretor.to_sql('director', engine, if_exists='append', index=False)
        print("Data sucessfully inserted into table director")
    except sqlalchemy.exc.IntegrityError:
        print('DatabaseDuplicate key entry error- the data exists already in the database')

def cleanRating():
    new_df = df[['rating']]
    #remove duplicates
    df_unique = new_df.drop_duplicates()
    #order df alphabetically
    df_unique = df_unique.sort_values('rating')
    # drop old index
    df_unique = df_unique.reset_index(drop=True)

    #open 2nd csv with description
    df_description = pd.read_csv(path_rating_description, encoding="UTF-8")
    #merge both df together and delete duplicate column
    combinedDf = df_unique.merge(df_description, how = 'left', left_on=['rating'], right_on=['rating_id_description'])
    del combinedDf['rating_id_description']

    # rename column
    combinedDf = combinedDf.rename(columns={'rating': 'rating_code'})

    try:
        # Convert dataframe to sql table
        combinedDf.to_sql('rating', engine, if_exists='append', index=False)
        print("Data sucessfully inserted into table rating")
    except sqlalchemy.exc.IntegrityError:
        print('DatabaseDuplicate key entry error- the data exists already in the database')

def createTableCountry():
    df_unique = cleanCountry()
    try:
        # Convert dataframe to sql table
        df_unique.to_sql('country', engine, if_exists='append', index=False)
        print("Data sucessfully inserted into table country")
    except sqlalchemy.exc.IntegrityError:
        print('DatabaseDuplicate key entry error- the data exists already in the database')

def cleanCountry():
    df_new = df[['country']]
    new_df = tidy_split(df_new, 'country', sep=',')
    #remove leading and trailing space of the column to remove duplicates
    new_df = new_df['country'].str.strip()
    #print(new_df)
    #remove duplicates
    df_unique = new_df.drop_duplicates()
    df_unique=df_unique.to_frame()
    #order df alphabetically
    df_unique = df_unique.sort_values('country')
    #delete empty row with only spaces
    df_unique = df_unique.drop([27])
    #drop old index
    df_unique = df_unique.reset_index(drop=True)
    #add index column
    df_unique['country_id'] = range(1, len(df_unique) + 1)
    #change order columns
    df_unique = df_unique[['country_id', 'country']]
    return df_unique

def createOneTable():
    df.to_sql('netflix_stage', engine, if_exists='append', index=False)
    print('In one big table "netflix_stage" sucessfully inserted')

#===========FUNCTIONS TO CREATE THE TABLES FOR N:M RELATIONS =========
def createShowCountryTable():
    df_new = df[['show_id','country']]
    new_df = tidy_split(df_new, 'country', sep=',')
    #remove leading and trailing space of the column to remove duplicates
    new_df['country'] = new_df['country'].str.strip()

    df_countryTable = cleanCountry()
    #rename column
    df_countryTable = df_countryTable.rename(columns={'country' : 'country2'})


    df_combined = new_df.merge(df_countryTable, how = 'left', left_on = ['country'], right_on = ['country2'])
    del df_combined['country2']
    del df_combined['country']

    try:
        # Convert dataframe to sql table
        df_combined.to_sql('show_country', engine, if_exists='append', index=False)
        print("Data sucessfully inserted into table show_country")
    except sqlalchemy.exc.IntegrityError:
        print('DatabaseDuplicate key entry error- the data exists already in the database')

def createShowDirectorTable():
    df_new = df[['show_id','director']]
    new_df = tidy_split(df_new, 'director', sep=',')
    #remove leading and trailing space of the column to remove duplicates
    new_df['director'] = new_df['director'].str.strip()
    df_director = cleanDirector()
    #rename column
    df_director = df_director.rename(columns={'director' : 'director2'})

    df_combined = new_df.merge(df_director, how = 'left', left_on = ['director'], right_on = ['director2'])
    del df_combined['director']
    del df_combined['director2']

    try:
        # Convert dataframe to sql table
        df_combined.to_sql('show_director', engine, if_exists='append', index=False)
        print("Data sucessfully inserted into table show_director")
    except sqlalchemy.exc.IntegrityError:
        print('DatabaseDuplicate key entry error- the data exists already in the database')

def createShowActorTable():
    df_new = df[['show_id','cast']]
    new_df = tidy_split(df_new, 'cast', sep=',')
    #remove leading and trailing space of the column to remove duplicates
    new_df['cast'] = new_df['cast'].str.strip()

    df_cast = cleanCast()
    #rename column
    #df_director = df_director.rename(columns={'director' : 'director2'})

    df_combined = new_df.merge(df_cast, how = 'left', left_on = ['cast'], right_on = ['actor'])
    del df_combined['cast']
    del df_combined['actor']

    #print(df_combined)
    try:
        # Convert dataframe to sql table
        df_combined.to_sql('show_actor', engine, if_exists='append', index=False)
        print("Data sucessfully inserted into table show_actor")
    except sqlalchemy.exc.IntegrityError:
        print('DatabaseDuplicate key entry error- the data exists already in the database')

def createShowGenreTable():
    df_new = df[['show_id', 'listed_in']]
    new_df = tidy_split(df_new, 'listed_in', sep=',')
    # remove leading and trailing space of the column to remove duplicates
    new_df['listed_in'] = new_df['listed_in'].str.strip()

    df_genre = cleanListedIn()
    # rename column
    # df_director = df_director.rename(columns={'director' : 'director2'})

    df_combined = new_df.merge(df_genre, how='left', left_on=['listed_in'], right_on=['genre'])
    del df_combined['listed_in']
    del df_combined['genre']

    print(df_combined)
    try:
        # Convert dataframe to sql table
        df_combined.to_sql('show_genre', engine, if_exists='append', index=False)
        print("Data sucessfully inserted into table show_genre")
    except sqlalchemy.exc.IntegrityError:
        print('DatabaseDuplicate key entry error- the data exists already in the database')

#========================READ MAIN CSV============================
df = pd.read_csv(path_netflix_csv, encoding = "UTF-8" )
#date_added was a string, shall be date-time format: September 9, 2016 --> 2016-09-09
df["date_added"]=df["date_added"].str.replace(",", "").str.strip() ## Strip removes spaces front and back
df["date_added"]=pd.to_datetime(df["date_added"], format="%B %d %Y")
df["date_added"]=df["date_added"].dt.date

#seperate season out of duration for tv-shows
df['season_count'] = df.apply(lambda x : x['duration'].split(" ")[0] if "Season" in x['duration'] else None, axis = 1)
#remove season from duration
df['duration'] = df.apply(lambda x : x['duration'].split(" ")[0] if "Season" not in x['duration'] else None, axis = 1)

df["director"]=df["director"].fillna("Unknown")
df["cast"]=df["cast"].fillna("Unknown")
df["country"]=df["country"].fillna("Unknown")


#==================CALL FUNCTIONS==================
'''
CreateShowsTable()

createGenreTable()
createCast()
createTableDirector()
cleanRating()
createTableCountry()

#tables for m:n relations
createShowCountryTable()
createShowDirectorTable()
createShowActorTable()
createShowGenreTable()
'''
print("test")


#for creating one big table just run this function
#createOneTable()