import json

data = 0
with open('bookData.json') as f:
    data = json.load(f)

price = 0
title = None
bookClass = None
myClass = None
maxBookCount = 0
bookCountClass = None
totalPrice = 0
highestCostClass = None
for classKey in data:
    myClass = data[classKey]
    if len(myClass) > maxBookCount:
        maxBookCount = len(myClass)
        bookCountClass = classKey
    bookPriceTotal = 0
    for book in myClass:
        if book['price']:
            bookPriceTotal+= book['price']
            if book['price'] > price:
                price = book['price']
                title = book['title']
                bookClass = classKey
    if bookPriceTotal > totalPrice:
        totalPrice = bookPriceTotal
        highestCostClass = classKey

print("The most expensive book required by the school is {} for ${} in {}".format(title, price, bookClass))
print("The class with the most required books is {} with {} books".format(bookCountClass, maxBookCount))
print("The class that cost the most to take was {} with ${} worth of books".format(highestCostClass, totalPriceesk))
