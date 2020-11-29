
#%% Imports
import pandas as pd

#%% Load each semester of class data into a data frame
classSheets = pd.ExcelFile("uvmClasses.xlsx")
semesters = classSheets.sheet_names

classDFs = {}
for semester in semesters:
    classDFs[semester] = classSheets.parse(semester)

#%% Drop unecessary columns
columnsToDrop = ['Max Enrl', 'Remain Seats', 'Begin Time', 'End Time', 'Days', 'Bldg', 'Room',
   'Instructor', 'PTRM', 'Inst Mthd', 'Attr', 'Fees', 'Section', 'Sect', 'Title']
for df in classDFs.values():
    for column in columnsToDrop:
        try:
            df.drop([column], axis=1, inplace=True)
        except:
            pass

#classDFs['Fall 2019'].head(30)

#%% Drop classes that are worth no credits
for df in classDFs.values():
    df.drop(df[df['Credits'] == " 0.00"].index, inplace = True)
    df.drop(df[df['Credits'] == 0].index, inplace = True)
    df.reset_index(drop=True, inplace = True)
    #we don't need credits after this
    df.drop(['Credits'], axis=1, inplace=True)

classDFs['Fall 2016'].shape

#%% Drop classes that don't have any students
for df in classDFs.values():
    df.drop(df[df['Cur Enrl'] == " 0"].index, inplace = True)
    df.drop(df[df['Cur Enrl'] == 0].index, inplace = True)
    df.reset_index(drop=True, inplace = True)

    #we don't need cur enrl after this
    df.drop(['Cur Enrl'], axis=1, inplace=True)

classDFs['Fall 2016'].shape

#%% clean up rows based on class names

#check if valid class name if not mark it with x to be dropped
def cleanClassNames(classRow):
    if not isinstance(classRow['Course'], str):
        #drop nulls
        classRow['Course'] = 'x'
        #print(classRow)
    else:
        stripedName = classRow['Course'].strip()
        words = stripedName.split()
        if len(words) < 2:
            #drop single words
            #print(classRow['Course'])
            classRow['Course'] = 'x'
        elif not words[1].isnumeric():
            #drop all that don't have a number as second word
            #print(classRow['Course'])
            classRow['Course'] = 'x'
        else:
            #this should be a valid class
            classRow['Course'] = words[0] + ' ' + words[1]
            #print(classRow['Course'])

    return classRow


for key, df in classDFs.items():
    #apply clean class names to every row
    df = df.apply(cleanClassNames, axis=1)

    #droped marked class rows and reset index
    df.drop(df[df['Course'] == 'x'].index, inplace = True)
    df.reset_index(drop=True, inplace = True)

    #save new dataframe
    classDFs[key] = df

#classDFs['Fall 2017'].head()

#%% Drop rows that are just alternate sections of the same class
for df in classDFs.values():
    df.drop_duplicates(subset=['Course'], inplace = True)
    df.reset_index(drop=True, inplace = True)

#classDFs['Fall 2016'].head(50)
#classDFs['Fall 2016'].shape


#%% Combine all dataframes into 1 only keeping the newest versions of classes
# are listed in multiple semesters
masterClassList = classDFs['Fall 2020']
masterClassList['Last Taught'] = 'Fall 2020'

for semester, df in classDFs.items():
    newClasses = df[~df['Course'].isin(masterClassList['Course'].values)]
    newClasses['Last Taught'] = semester
    #print(newClasses.shape)
    masterClassList = pd.concat([masterClassList, newClasses])
    #print(masterClassList.shape)

masterClassList.sort_values(by=['Course'], inplace = True)
masterClassList.head(50)

#%% Final cleaning and write out to csv and write comments to text
masterClassList.to_csv("masterClassList.csv", index=False,)
masterClassList['Comments'].to_csv("comments.txt", index=False, header=False)
