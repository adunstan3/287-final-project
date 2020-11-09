#import stuff
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import copy

#get the horibly structured data off of the site
def getSemestersData(link, comentsLoc):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    pageContents = soup.find("pre").contents
    print(len(pageContents))

    pageText = soup.find("pre").get_text()
    lines = pageText.splitlines(False)

    rawHeads = lines[1]
    columnTitals = rawHeads.split()
    titalPositions = []

    for head in columnTitals:
        startOfHead = rawHeads.find(head)

        #some column heads are missaligned with the data so
        if head == "Days":
            startOfHead-= 1
        elif head == "Credits":
            startOfHead-= 1
        elif head == "Max":
            startOfHead-= 1
        elif head == "Cur":
            startOfHead-= 1
        elif head == "Bldg":
            startOfHead-= 1
        elif head == "Remain":
            startOfHead-= 1
        elif head == "Room":
            startOfHead-= 1
        elif head == "Instructor":
            startOfHead-= 1
        elif head == "Fees":
            startOfHead-= 1
        elif head == "Comments":
            startOfHead = comentsLoc

        titalPositions.append(startOfHead)
        #print("{} is at position {}".format(head, startOfHead))

    columnTitals.append("Department")
    print(columnTitals)
    currentDepartment = ""
    data = {}
    storedLineData = [""] * len(columnTitals)

    for lineNum in range(2, len(lines)):
        lineToProcess = lines[lineNum]

        #if this line declares the current department store that data and don't split words
        if ">>>====>" in lineToProcess:
            department = lineToProcess.strip()
            department = department[8:-8]
            department = department.replace("  ", "--")
            department = department.replace(" ", "")
            currentDepartment = department
            continue

        #if this line is blank don't process it
        if lineToProcess.isspace():
            continue

        #this line contains data split it and put it in the correct columns
        lineWords = lineToProcess.split()
        lineData = [""] * len(columnTitals)
        for word in lineWords:
            wordPosition = lineToProcess.find(word)

            #replace the found word with a blank space the same size
            #this helps the code deal with duplicate words in the same line
            lineToProcess = lineToProcess.replace(word, (" "*len(word)) , 1)

            wordColumn = titalPositions[0]
            for column in titalPositions:
                if column <= wordPosition:
                    wordColumn = column

            #some of the column titals go onto the second line so grab that data
            if lineNum == 2:
                columnTitals[titalPositions.index(wordColumn)] += " " + word

            #this is regular class data, grab it and add it to the line data
            else:
                lineData[titalPositions.index(wordColumn)] += " " + word

        lineData[columnTitals.index("Department")] = currentDepartment

        if lineNum == 2:
            for tital in columnTitals:
                data[tital] = []
        else:
            if lineData[columnTitals.index('CRN')]:
                #push stored line data to data
                for tital in columnTitals:
                    data[tital].append(storedLineData[columnTitals.index(tital)])

                #store the current data
                storedLineData = lineData
            else:
                #there is no CRN in this line so it isn't a class line
                #it is a line that has class data that takes up multiple lines
                #append the data in this line to the stored data to make a complete class line
                for i in range(len(lineData)):
                    if lineData[i] and columnTitals[i] != "Department":
                        storedLineData[i] += " " + lineData[i]

    #push the last stored class to the data
    for tital in columnTitals:
        data[tital].append(storedLineData[columnTitals.index(tital)])

    #Now fill in blank spaces for course and title duplicates
    storedCourse = ""
    storedTitle = ""
    for classNum in range(len(data["CRN"])):
        if not data["Course"][classNum] == "":
            storedCourse = data["Course"][classNum]
        else:
            data["Course"][classNum] = storedCourse
        if not data["Title"][classNum] == "":
            storedTitle = data["Title"][classNum]
        else:
            data["Title"][classNum] = storedTitle

    df = pd.DataFrame (data, columns = columnTitals)
    return df

with pd.ExcelWriter('uvmClasses.xlsx') as writer:
    df = getSemestersData('https://giraffe.uvm.edu/~rgweb/batch/swrsectc_fall_soc_202009/all_sections.html', 154)
    df.to_excel(writer, sheet_name= 'Fall 2020', index=False)
    df = getSemestersData('https://giraffe.uvm.edu/~rgweb/batch/swrsectc_spring_soc_202001/all_sections.html', 154)
    df.to_excel(writer, sheet_name= 'Spring 2020', index=False)
    df = getSemestersData('https://giraffe.uvm.edu/~rgweb/batch/swrsectc_fall_soc_201909/all_sections.html', 141)
    df.to_excel(writer, sheet_name= 'Fall 2019', index=False)
    df = getSemestersData('https://giraffe.uvm.edu/~rgweb/batch/swrsectc_spring_soc_201901/all_sections.html', 141)
    df.to_excel(writer, sheet_name= 'Spring 2019', index=False)
    df = getSemestersData('https://giraffe.uvm.edu/~rgweb/batch/swrsectc_fall_soc_201809/all_sections.html', 141)
    df.to_excel(writer, sheet_name= 'Fall 2018', index=False)
    df = getSemestersData('https://giraffe.uvm.edu/~rgweb/batch/swrsectc_spring_soc_201801/all_sections.html', 141)
    df.to_excel(writer, sheet_name= 'Spring 2018', index=False)
    df = getSemestersData('https://giraffe.uvm.edu/~rgweb/batch/swrsectc_fall_soc_201709/all_sections.html', 141)
    df.to_excel(writer, sheet_name= 'Fall 2017', index=False)
    df = getSemestersData('https://giraffe.uvm.edu/~rgweb/batch/swrsectc_spring_soc_201701/all_sections.html', 141)
    df.to_excel(writer, sheet_name= 'Spring 2017', index=False)
    df = getSemestersData('https://giraffe.uvm.edu/~rgweb/batch/swrsectc_fall_soc_201609/all_sections.html', 141)
    df.to_excel(writer, sheet_name= 'Fall 2016', index=False)
    df = getSemestersData('https://giraffe.uvm.edu/~rgweb/batch/swrsectc_spring_soc_201601/all_sections.html', 141)
    df.to_excel(writer, sheet_name= 'Spring 2016', index=False)
