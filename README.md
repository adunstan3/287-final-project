# 287-final-project
Bookstore data and class visualiser

- bookStoreScraping.py is the selenium bot code
- bookData.json is the book store data produced by the bot
- bookDataReader.py is a short little program that pulls some fun facts from the bookstore data

Bookstore site: https://uvmbookstore.uvm.edu/buy_textbooks.asp

Hello! I added the text below the Monday morning after the due date, so ignore it for grading if you need to. Have a good day!

The bookstore scraper was a lot harder to write than I first anticipated. The site is broken into two pages, one with the class input and one with the book information. None of the selection data or the book data is contained in the URL, so I couldn't navigate the data by editing the URLs. It also means I couldn't duplicate pages or save old page states by keeping links. Every time I finished inputting class data, I had to go to a new page to get the book data and hit the back button to go back to the selection page. This refresh is a problem because it destroys and recreates all of the HTML elements I interacted with. This means I had to refind all of the HTML elements every time I got book data, or my program would crash with a stale elements exception. 

I couldn't solve all of the stale element bugs, so instead of going on a goose chase, I build my program to accommodate the selenium bot failing. This was an exciting approach, and the first time I have done anything like this in my code. I wrote the search bots so that they can start from any point in the class search tree. When one bot died, I would start another bot one step back in the search tree and have it continue writing the data. The final scrape took around ten bots to get through all the data, and this method was less painful than hunting down seemingly random selenium bugs. 

When I have free time, I might edit the scraper to grab ISBNs as well. This would not be too difficult, and it would let me get extra info about books. I don't need any additional information for this project, but I would like to answer how many teachers make students buy books that they have written. ISBNs would allow me to get the author's name quickly, and I could check that against the registrar data for who teaches what class. 
