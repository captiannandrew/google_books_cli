#!/usr/bin/env python
import json,requests
import sys
import csv
import operator
import datetime


#f = open("library.csv", "w")
#f.truncate()
#f.close()

class searchAPI():
    def __init__(self):
       url = 'https://www.googleapis.com/books/v1/volumes'
       self.url = url 
    def getBooks(self): 
        total_books = 0
        library = []
        already_have = []

        while total_books <= 200:   
            #ask user 
            book_subject = raw_input("Search Google Books API for :") 
            if book_subject not in already_have:
                already_have.append(book_subject)
            else:
                book_subject = raw_input("Libray already contains subject,Search Google Books API for :") 
            
            #number of books in library conditions
            total_books += 40
            
            #get books from google
            payload = {'q': book_subject, 'maxResults': '40'}
            r = requests.get( self.url, params=payload)
            
            # json objects placed in library
            lib = r.json()
            #access list of books information
            library.append(lib)
    
            # minimum book amount check
            if total_books >= 100:
                response = raw_input('Would you like to add more books to library? Y/N')
                if response == 'n' or "no":
                    break
                elif response =='y' or "yes":
                    return getBooks(self)
            self.items = library
    def group_publisher(self):
        print '\033[4mPrinting Grouping By Publisher\033[0m'
        #group by publisher
        publisher_dict ={}
        for x,name in enumerate(self.items):
                #item= self.library[bookindex]
            if 'publisher' in name['items'][0]['volumeInfo']:
                publisher_id = name['items'][0]['volumeInfo']['publisher']
            else:
                print 'Publish does not exist for %s' % name['items'][0]['id']
            if publisher_id not in publisher_dict:
                publisher_dict[publisher_id] = [name]
            elif publisher_id in publisher_dict:
                publisher_dict[publisher_id].append(name)
        for publisher in publisher_dict:
            print publisher
            for book in publisher_dict[publisher]:
                print book['items'][0]['volumeInfo']['title']

    def group_pdf_availability(self):
        print '\033[4mPrinting Grouping By PDF Availability\033[0m'
            #group by pdf availability
        pdf_dict ={}
        for x,item in enumerate(self.items):
            pdf_availablity = item['items'][0]['accessInfo']['pdf']['isAvailable']
            if pdf_availablity not in pdf_dict:
                pdf_dict[pdf_availablity] = [item]
            elif pdf_availablity in pdf_dict:
                pdf_dict[pdf_availablity].append(item)
        for pdf_availablity in pdf_dict:
            print pdf_availablity
        for book in pdf_dict[pdf_availablity]:
            print book['items'][0]['volumeInfo']['title'] 

    def group_epub_availability(self):
        print '\033[4mPrinting Grouping By ePub Availability\033[0m'
            #group by epub availability
        epub_dict ={}
        for x,item in enumerate(self.items):
            epub_availablity = item['items'][0]['accessInfo']['epub']['isAvailable']
            if epub_availablity not in epub_dict:
                epub_dict[epub_availablity] = [item]
            elif epub_availablity in epub_dict:
                epub_dict[epub_availablity].append(item)
        for epub_availablity in epub_dict:
            print epub_availablity
            for book in epub_dict[epub_availablity]:
                print book['items'][0]['volumeInfo']['title'] 

    def group_Ebook_avaiability(self):
        print '\033[4mPrinting Grouping By eBook Availability\033[0m'
            #group by Ebook availability
        ebook_dict ={}
        for x,item in enumerate(self.items):
            ebook_availablity = item['items'][0]['saleInfo']['isEbook']
            if ebook_availablity not in ebook_dict:
                ebook_dict[ebook_availablity] = [item]
            elif ebook_availablity in ebook_dict:
                ebook_dict[ebook_availablity].append(item)
        for ebook_availablity in ebook_dict:
            print ebook_availablity
            for book in ebook_dict[ebook_availablity]:
                print book['items'][0]['volumeInfo']['title'] 

    def sort_by_PubDate(self):
        print '\033[4mPrinting by Publication Date\033[0m'
        #sort book by published date
        published_fulldate_list = []
        published_yearonly_list =[]
        published_yearmonth_list =[]   
        for x,item in enumerate(self.items):
            if 'publishedDate' not in item['items'][0]['volumeInfo']:
                print 'Book ID: %s does not have a published date' % item['items'][0]['id']
            if  len(item['items'][0]['volumeInfo']['publishedDate']) == 4:
                published_yearonly_list.append(item['items'][0])
            if  len(item['items'][0]['volumeInfo']['publishedDate']) == 7:
                published_yearmonth_list.append(item['items'][0])
            else: 
                published_fulldate_list.append(item['items'][0])  
        #year and month only sorting
        sorted_yearmonth_books = sorted(published_yearmonth_list, key=lambda book: datetime.datetime.strptime(book['volumeInfo']['publishedDate'], '%Y-%m'))
        for book in sorted_yearmonth_books:
            print '%s =>%s' % (book['volumeInfo']['title'], book['volumeInfo']['publishedDate'])

       
        #year only sorting
        sorted_yearDate_books = sorted(published_yearonly_list, key=lambda book: datetime.datetime.strptime(book['volumeInfo']['publishedDate'], '%Y'))
        for book in sorted_yearDate_books:
            print '%s =>%s' % (book['volumeInfo']['title'], book['volumeInfo']['publishedDate'])
                        
        #full date sorting   
        sorted_publishedDate_books = sorted(published_fulldate_list, key=lambda book: datetime.datetime.strptime(book['volumeInfo']['publishedDate'], '%Y-%m-%d'))
        for book in sorted_publishedDate_books:
            print '%s =>%s' % (book['volumeInfo']['title'], book['volumeInfo']['publishedDate']) 

    def _sort_saleability(self):
            #sort books by saleability
        self.price_list=[]
        not_for_sale_list = []
        for x,item in enumerate(self.items):
            if item['items'][0]['saleInfo']['saleability'] == 'NOT_FOR_SALE':
                not_for_sale_list.append(item['items'][0])
            elif item['items'][0]['saleInfo']['saleability'] == 'FOR_SALE':
                self.price_list.append(item['items'][0])
        return self.price_list        

    def sort_by_listprice(self):
        print '\033[4mPrinting by List Price\033[0m'
            # sort books by listprice
        self._sort_saleability()
        sorted_listPrice_books = sorted(self.price_list, key=lambda book: book['saleInfo']['listPrice']['amount']) 
        for book in sorted_listPrice_books:
            print "%s => %d" % (book['volumeInfo']['title'], book['saleInfo']['listPrice']['amount'])

    def sort_by_retailPrice(self):
        print '\033[4mPrinting by Retail Price \033[0m'
        self._sort_saleability()
            #sort books by retailprice
        sorted_retailPrice_books = sorted(self.price_list, key=lambda book: book['saleInfo']['retailPrice']['amount']) 
        for book in sorted_retailPrice_books:
            print "%s => %d" % (book['volumeInfo']['title'], book['saleInfo']['retailPrice']['amount'])

    def sort_by_averagerating(self):
        print '\033[4mPrinting by Average Rating \033[0m'
            #sort books by average rating
        averageRating_list = []
        for x,item in enumerate(self.items):
            if 'averageRating' not in item['items'][0]['volumeInfo']:
                print "Book ID: %s does not have average rating" % item['items'][0]['id']
            else:
                averageRating_list.append(item)
        average_sorted_books = sorted(averageRating_list, key=lambda book: book['items'][0]['volumeInfo']['averageRating'])
        for book in average_sorted_books:
            print '%s => %d' % (book['items'][0]['volumeInfo']['title'], book['items'][0]['volumeInfo']['averageRating'])

    def sort_by_ratingCount(self):
        print '\033[4mPrinting by  Rating Count \033[0m'
            #sort books by rating count
        rating_count_list =[]
        for x,item in enumerate(self.items):
            if 'ratingsCount' not in item['items'][0]['volumeInfo']:
                print "Book ID: %s does not have rating Count" % item['items'][0]['id']
            else:
                rating_count_list.append(item)
        ratingCount_sorted_books = sorted(rating_count_list, key=lambda book: book['items'][0]['volumeInfo']['ratingsCount'])
        for book in ratingCount_sorted_books:
            print '%s => %d' % (book['items'][0]['volumeInfo']['title'], book['items'][0]['volumeInfo']['ratingsCount'])

    def sort_by_pageCount(self):
        print '\033[4mPrinting by Page Count \033[0m'
            #sort books by pageCount
        pageCount_list =[]
        for x,item in enumerate(self.items):
            if 'pageCount' not in item['items'][0]['volumeInfo']:
                print 'Book ID: %s does not have page count' % item['items'][0]['id']
            else:
                pageCount_list.append(item)
        sorted_pageCount_books = sorted(pageCount_list, key=lambda book: book['items'][0]['volumeInfo']['pageCount'])
        for book in sorted_pageCount_books:
            print '%s => %d' % (book['items'][0]['volumeInfo']['title'], book['items'][0]['volumeInfo']['pageCount'])
    
    def _save_csv_file(self):
        with open('library.csv', 'wb',) as f:
            w = csv.writer(f)
            w.writerows(self.items.items())

    def _load_csv_file(self):
         reader = csv.reader(f)        
         for row in reader:
            print(row)  
if __name__== "__main__":
    main = searchAPI()
    main.getBooks()
    main.group_publisher()
    main.group_pdf_availability()
    main.group_epub_availability()
    main.group_Ebook_avaiability()
    main.sort_by_PubDate()
    main.sort_by_listprice()
    main.sort_by_retailPrice()
    main.sort_by_averagerating()
    main.sort_by_ratingCount()
    main.sort_by_pageCount()
    
