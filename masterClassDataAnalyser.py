#%% Imports
import pandas as pd

#%% Load master class CSV
classList = pd.read_csv('Data/masterClassList.csv')
classList.head()

#%% Gather some class size statistics
avgMaxEnrl = classList['Max Enrl'].mean()
avgCurEnrl = classList['Cur Enrl'].mean()
avgPercentEnrl = avgCurEnrl / avgMaxEnrl * 100

print("The average maximum capacity for a class is {:.2f}".format(avgMaxEnrl))
print("The average actual size of a class is {:.2f}".format(avgCurEnrl))
print("The average class is {:.2f}% full".format(avgPercentEnrl))

#uvm has 18:1 student teacher ratio so this seems pretty acurate

numClasses = classList['Cur Enrl'].count()
numUnder20 = classList[classList['Cur Enrl'] < 20]['Cur Enrl'].count()
percentUnder20 = numUnder20/numClasses * 100
print("{:.2f}% of the classes had under 20 students in them".format(percentUnder20))

numClasses = classList['Max Enrl'].count()
numUnder20 = classList[classList['Max Enrl'] < 20]['Max Enrl'].count()
percentUnder20 = numUnder20/numClasses * 100
print("{:.2f}% of the classes had a max size of under 20 students".format(percentUnder20))

# Uvm claims 48.7% of classes fewer than 20 students

#%% Gather some department statistics
deparmentClasses = classList['Department'].value_counts()

#157 class categories in the registrar

pd.set_option("display.max_rows", None, "display.max_columns", None)
print(deparmentClasses)

# The registrar splits the courses up by categories with 157 categories in total
# The category with the most offered classes was EUROPEAN--STUDIES with 108
# classes, this was followed by
# music, environmental studies, business admin, and english.
# Mathematics and cs had 57 classes, stats had 32, and complex systems had 10
