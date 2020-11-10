# 287-final-project
Bookstore data and class visualiser

### Files
- bookStoreScraping.py is the selenium bot code to scrape the bookstore
- bookData.json is the book store data produced by the bot
- bookDataReader.py is a short little program that pulls some fun facts from the bookstore data
- classDataScraper.ipynb is the code that grabs and formats the registrar data
- uvmClasses.xlsx is an excell document with the web data from the past 10 semesters in different pages

### Links
- Bookstore site: https://uvmbookstore.uvm.edu/buy_textbooks.asp
- Registrar site: https://giraffe.uvm.edu/~rgweb/batch/swrsectc_fall_soc_202009/all_sections.html
- Undergraduate population source: https://tinyurl.com/y5b8npzu

### Fun facts found so far
- The most expensive required book this semester was a 402 dollar biochem textbook. 
- The class with the most required books was classics 095 with 11 required books. 
- The most expensive class to take was human development 263, with 491 dollars of required books.
- There are a lot of "offered" classes that are completely empty. The average class size for this semseter was .1 students per class. 
- The total money the school asked all students to pay was $4,069,907.61 
- The school asked the average student to spend: $355.67

### Week 3 update:

This week I converted the JSON data from the bookstore into a tabular format and added it to the class data. I then used that data to get an estimate of the average amount each student spends on books. It was challenging to get the two data sets to merge, but it wasn’t too hard to get my estimate once they were merged. 
I matched the book prices to the classes, and then I multiplied the price by the current enrolment to find the total spent on books by the class. I then added up all the totals for all classes to find the total spent on books by the school. I then divided that number by the total undergraduate population to get the average amount spend on books by each student. 


### Week 2 update:

The major milestone I accomplished this week was loading all of the class data I will need into pandas data frames and saving it to an excel file. This turned out to be significantly harder than predicted. The registrar page doesn’t hold the data in any table. It is one pre tag with all the pre-formatted text interrupted by a tags for the links.

The structure made it harder to write to a data frame, so I used soup’s get text function and processed the raw text. I ended up splitting the data by lines, then splitting each line into words. I then searched the line for each word to get its location. I had thresholds to determine which column the word fit into, then I would add the word in question to any other words in that column. I had to save old line data for a couple of lines because some classes have data that extends to several lines below the line it starts on.

I also had to deal with blank lines and lines that tell you what department each class is in. Some manual tweaking needed to be done because sometimes the column headings didn’t line up with the data they were describing. In the end, I created a fairly general system because it took me a couple of hours to successfully scrape one semester but then only 30 minutes to get all ten semesters that I need.


### Week 1 update:

The bookstore scraper was a lot harder to write than I first anticipated. The site is broken into two pages, one with the class input and one with the book information. None of the selection data or the book data is contained in the URL, so I couldn't navigate the data by editing the URLs. It also means I couldn't duplicate pages or save old page states by keeping links. Every time I finished inputting class data, I had to go to a new page to get the book data and hit the back button to go back to the selection page. This refresh is a problem because it destroys and recreates all of the HTML elements I interacted with. This means I had to refind all of the HTML elements every time I got book data, or my program would crash with a stale elements exception.

I couldn't solve all of the stale element bugs, so instead of going on a goose chase, I build my program to accommodate the selenium bot failing. This was an exciting approach, and the first time I have done anything like this in my code. I wrote the search bots so that they can start from any point in the class search tree. When one bot died, I would start another bot one step back in the search tree and have it continue writing the data. The final scrape took around ten bots to get through all the data, and this method was less painful than hunting down seemingly random selenium bugs.

When I have free time, I might edit the scraper to grab ISBNs as well. This would not be too difficult, and it would let me get extra info about books. I don't need any additional information for this project, but I would like to answer how many teachers make students buy books that they have written. ISBNs would allow me to get the author's name quickly, and I could check that against the registrar data for who teaches what class.
