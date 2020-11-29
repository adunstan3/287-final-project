#%% Imports
import pandas as pd

#%% Load master class CSV
classList = pd.read_csv('Data/masterClassList.csv')
classList.head()

#%% process pre and co reqs
def findPreCo(row):
    comment = row['Comments']
    for requirement in comment.split(';'):
        if ' Coreq' in requirement:
            coreqs = requirement[requirement.find('Coreq'):]
            coreqs = coreqs[coreqs.find(':')+1:]
            coreqs = coreqs.replace('Coreq', '')
            coreqs = coreqs.replace(' &', ',')
            coreqs = coreqs.replace(' and', ',')
            coreqs = coreqs.replace(' or ', '/')
            coreqs = coreqs.replace(',,', ',')

            titles = coreqs.split(',')
            coreqs = ''
            for title in titles:
                title = title.split()[0]
                if len(title.split()) > 1:
                    title += title.split()[1]
                coreqs += title +', '

            print(coreqs)

classList.apply(findPreCo, axis=1)
