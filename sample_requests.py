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
print id_list

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
    if publisher_id is not in publisher_dict:
        publisher_dict.append(publisher_id:[item])
    if publisher_id is in publisher_dict:
        publisher_dict.append(publisher_id:
        



#if 'publisher' in items[0]['volumeInfo']:
 #   print items[0]['volumeInfo']['publisher']