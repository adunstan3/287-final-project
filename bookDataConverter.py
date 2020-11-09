import json
import pandas as pd

#--------------------------------------------------------------------
#format the book data json into a data frame

#read in the json
with open('bookData.json') as f:
    classDict = json.load(f)

#prepare the structure used to write the data to the dataframe
data = {"title" : [], "section" : [], "totalPrice" : []}

classNames = classDict.keys()
numPrinted = 0

for dictKey in classNames:
    #Grab and format class name
    className = dictKey[:dictKey.find(',')]
    className = className.replace('- ', '')

    #grab total price of books for this class
    totalPrice = 0
    for book in classDict[dictKey]:
        if book["price"]:
            totalPrice += book["price"]

    #remove the class title from the working string
    tempDictKey = dictKey[dictKey.find(',')+2:]

    #grab each section in the working string untill none are left
    while tempDictKey[0] != '(': #when we get to the '(' we have found all sections
        commaPosition = tempDictKey.find(',')
        parenPosition = tempDictKey.find('(')
        section = ''

        #if there is still a comma before the ( this is not the last section
        if commaPosition != -1 and commaPosition < parenPosition:
            section = tempDictKey[: commaPosition]
            tempDictKey = tempDictKey[commaPosition+1:]
        #this is the last section
        else:
            section = tempDictKey[: parenPosition]
            tempDictKey = tempDictKey[parenPosition:]

        #remove the section word, and the whitespace
        section = section.replace('section', '')
        section = section.strip()

        #write the section's data to the data dict
        data['title'].append(className)
        data['section'].append(section)
        data['totalPrice'].append(totalPrice)

#convert the data dict to a data frame and save it
df = pd.DataFrame(data=data)
df.to_excel("bookPrices.xlsx", index=False)
