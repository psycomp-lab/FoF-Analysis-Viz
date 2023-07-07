import os 
import pandas as pd
# get all the csv files from the dataset that are related to a specific movement
# each movement may have multiple repetitions
def get_movement_files(m):
    directory = '/home/Lucian/Github/Thesis/FoF-Analysis-Viz/dataset'
    files = {}
    for patients in os.listdir(directory):
        f = os.path.join(directory, patients)
        if patients.startswith('P'):
            if patients not in files:
                files[patients] = []
        if os.path.isdir(f):
            for movement in os.listdir(f):
                g = os.path.join(f, movement)
                if os.path.isdir(g) and movement == m:
                    for repetition in os.listdir(g):
                        h = os.path.join(g, repetition)
                        if os.path.isdir(h):
                            for file in os.listdir(h):
                                if file.endswith('.csv'):
                                    result = os.path.join(h, file)
                                    files[patients].append(result)     
    # sort the patients by the endidng number of their name
    files = dict(sorted(files.items(), key=lambda item: item[0][1:]))           
    return files

# list the files 
def list_files(files):
    for patient, movements in files.items():
        print(patient)
        for movement in movements:
            print('\t', movement)
# get the dataframes from each file and keep only the columns needed 
def get_dataframe_from_file(files, columns_needed):
   dataframes = {}
   for patient, movements in files.items():
       if patient not in dataframes:
           dataframes[patient] = []
       for movement in movements:
           df = pd.read_csv(movement, sep=';')
           df = df[columns_needed]
           dataframes[patient].append(df)
   return dataframes     

def get_tuple_from_row(df, x, y, z):
    return df[[x, y, z]].apply(tuple, axis=1)

def get_values_from_df(dataframes, x, y, z):
    values = {}
    for patient, movements in dataframes.items():
        if patient not in values:
            values[patient] = []
        for movement in movements:
            result = get_tuple_from_row(movement, x, y, z)
            if result is not None:
                values[patient].append(result)
    return values