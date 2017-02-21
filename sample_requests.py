#!/usr/bin/env python
import json,requests
import sys
import csv

book_subject = raw_input("Search Google Books API for :") 
num_books = raw_input('Enter how many books you would like to see:' )

#if total_books < 100 or total_books > 200:
 #   print "Your library must have atleast 100 books and no more the 200."
 #  sys.exit(1)


payload = {'q': book_subject, 'maxResults': num_books}
    #get call
r = requests.get('https://www.googleapis.com/books/v1/volumes', params=payload)
library = r.json()
items = library['items']

#make a list called id list and as you loop throguh that items list and store it into id list and check
#if the next one is in the first one if not store
id_list =[]
for item in items:
    item_id = item['id']
    if item_id not in id_list:
        id_list.append(item_id) 
    else:
        print "%s is already in the list!" % item_id

#writes library as a csv file and then reads it

with open('library.csv', 'wb',) as f:
    w = csv.writer(f)
    w.writerows(library.items())

with open('library.csv', 'rb') as f:
    reader = csv.reader(f)
    #for row in reader:
        #print(row)

#group by publisher
publisher_dict ={}
for item in items:
    publisher_id = item['volumeInfo']['publisher']
    if publisher_id not in publisher_dict:
        publisher_dict[publisher_id] = [item]
    elif publisher_id in publisher_dict:
        publisher_dict[publisher_id].append(item)
for publisher in publisher_dict:
    print publisher
    for book in publisher_dict[publisher]:
        print book['volumeInfo']['title']

#group by pdf availability
pdf_dict ={}
for item in items:
    pdf_availablity = item['accessInfo']['pdf']['isAvailable']
    if pdf_availablity not in pdf_dict:
        pdf_dict[pdf_availablity] = [item]
    elif pdf_availablity in pdf_dict:
        pdf_dict[pdf_availablity].append(item)
for pdf_availablity in pdf_dict:
    print pdf_availablity
    for book2 in pdf_dict[pdf_availablity]:
        print book2['volumeInfo']['title'] 

#group by epub availability
epub_dict ={}
for item in items:
    epub_availablity = item['accessInfo']['epub']['isAvailable']
    if epub_availablity not in epub_dict:
        epub_dict[epub_availablity] = [item]
    elif epub_availablity in epub_dict:
        epub_dict[epub_availablity].append(item)
for epub_availablity in epub_dict:
    print epub_availablity
    for book3 in epub_dict[epub_availablity]:
        print book3['volumeInfo']['title'] 

#group by Ebook availability

ebook_dict ={}
for item in items:
    ebook_availablity = item['saleInfo']['isEbook']
    if ebook_availablity not in ebook_dict:
        ebook_dict[ebook_availablity] = [item]
    elif ebook_availablity in ebook_dict:
        ebook_dict[ebook_availablity].append(item)
for ebook_availablity in ebook_dict:
    print ebook_availablity
    for book4 in ebook_dict[ebook_availablity]:
        print book4['volumeInfo']['title'] 



     

#if 'publisher' in items[0]['volumeInfo']:
 #   print items[0]['volumeInfo']['publisher']