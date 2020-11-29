from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json

DRIVER_PATH = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

driver.get('https://uvmbookstore.uvm.edu/buy_textbooks.asp')
driver.implicitly_wait(3)

selectionDept = 0
selectionCourse = 0
selectionSection = 0
selections = ['fDept', 'fCourse', 'fSection']
selectionsNames = ["Department", "Course", "Section"]

currentDeptNum = 0
currentCourseNum = 0

classNum = 0

previousDepth = 0
currentDepth = 0
driver.find_element_by_xpath("//select[@id='fTerm']/option[2]").click()


def selectOptions(selectionType):
    global currentDeptNum, currentCourseNum, previousDepth, currentDepth

    #wait till the selection options load by trying to find the second option
    print(selections[selectionType])
    driver.find_element_by_xpath("//select[@id='{}']/option[2]".format(selections[selectionType]))

    #grab the options of the current selector we are iterating through
    options = Select(driver.find_element_by_id(selections[selectionType])).options
    numOptions = len(options)-1

    print("Select Options called! Type: {}, Length: {}".format(selectionsNames[selectionType], numOptions))

    myRange = 0
    if selectionsNames[selectionType] == "Department":
        myRange = range(previousDepth, numOptions)
    else:
        myRange = range(numOptions)

    for optionNumber in myRange:
        driver.find_element_by_xpath("//select[@id='{}']/option[2]".format(selections[selectionType]))

        #Select the current option
        currentName = Select(driver.find_element_by_id(selections[selectionType])).options[optionNumber+1].text
        print("Type: {}, option: {}".format(selectionsNames[selectionType], currentName))

        Select(driver.find_element_by_id(selections[selectionType])).select_by_index(optionNumber+1)

        if selectionType == 2: #you have selected every option and filled out the form click the button
            submitSelections()
            driver.find_element_by_xpath("//select[@id='fTerm']/option[2]").click()
            driver.find_element_by_xpath("//select[@id='fDept']/option[{}]".format(currentDeptNum)).click()
            driver.find_element_by_xpath("//select[@id='fCourse']/option[{}]".format(currentCourseNum)).click()
        else:
            if selectionType == 0:
                currentDeptNum = optionNumber+2
                currentDepth += 1

            if selectionType == 1:
                currentCourseNum = optionNumber+2

            #you have not selected every option and filled out the form
            selectOptions(selectionType+1)

    print("Select Options Finished! Type: {}, Length: {}".format(selectionsNames[selectionType], numOptions))

def submitSelections():
    global classNum
    driver.find_element_by_id('tbe-add-section').click()
    driver.find_element_by_id('generate-book-list').click()

    classInfo = driver.find_element_by_id("course-bookdisplay-coursename").text
    data[classInfo] = []
    pickOneBook = {'title': None, 'price': 10000000}

    for bookRow in driver.find_elements_by_class_name("book-container"):
        bookTital = bookRow.find_element_by_class_name("book-title").text
        bookPrice = None
        if bookRow.find_elements_by_class_name("book-price-list"): #there is a price so grab it slicing off the $
            bookPrice = float(bookRow.find_elements_by_class_name("book-price-list")[0].text[1:])

        if bookRow.find_elements_by_class_name("book-req")[0].text == 'Required':
            data[classInfo].append({'title': bookTital, 'price': bookPrice})

        elif bookRow.find_elements_by_class_name("book-req")[0].text == 'Pick One': #isRequiredList isn't empty which means the book is required
            #print(isRequiredList[0].text)
            if bookPrice:
                if bookPrice < pickOneBook['price']:
                    pickOneBook = {'title': bookTital, 'price': bookPrice}

    if pickOneBook['title']:
        data[classInfo].append(pickOneBook)

    print(data[classInfo])

    driver.back()

data = {}

def grabData():
    global previousDepth, currentDepth
    try:
        selectOptions(0)
    except:
        print("currentDepth: {}".format(currentDepth))
        previousDepth = currentDepth - 1
        currentDepth = previousDepth
        grabData()

grabData()

with open('Data/bookData.json', 'a') as outfile:
    json.dump(data, outfile)

driver.close()
