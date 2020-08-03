# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 13:52:09 2020

@author: Daria
"""
import os
import os.path
import string
import pandas as pd
import matplotlib.pyplot as plt

book_dir = r"C:\Users\Daria\Documents\PythonScripts\Books"

def count_words(lorem_ipsum):
    word_count = {}
    lorem_ipsum = lorem_ipsum.lower()
    '''Takes unique words from a string and counts number of occurrences'''    
    lorem_ipsum = lorem_ipsum.translate(str.maketrans('', '', string.punctuation))    
    lorem_ipsum = lorem_ipsum.replace('\n',' ').replace('\r', ' ')
    for word in lorem_ipsum.split(' '):        
        if word in word_count:
            word_count[word] += 1            
        else:
            word_count[word] = 1
    return word_count   

# def count_words_fast(text):
    # '''Takes unique words from a string and counts number of occurrences. Removes punctuation'''  
    # lorem_ipsum = read_book(title)
    # lorem_ipsum = lorem_ipsum.lower()     
    # lorem_ipsum = lorem_ipsum.translate(str.maketrans('', '', string.punctuation))
    # print(lorem_ipsum) 
    # word_counts = Counter(lorem_ipsum.split(" "))
    # return word_counts
 
def read_book(title_path): 
    """ 
    Reads a book from a file provided in the path
    Parameters
    ----------
    title_path : path to file
    Returns
    -------
    lrm : file with removed backspaces.
    """
    #title_path = os.path.abspath(title_path)
    #print (title_path)
    with open(title_path,'r', encoding='utf-8') as current_file:    
        lrm = current_file.read()       
    lrm = lrm.replace('\n',' ').replace('\r', ' word')    
    return lrm

#ind = text.find("What's in a name?")
#print (ind)
#print (text[ind:ind+1000])

def word_stats(word_count):
    """    
    Parameters
    ----------
    word_count : takes value from function that reads a book file and counts number or unique words.

    Returns in a tuple
    -------
    num_uniq : number of unique words in a given book file.
    wrdcnt : values of said words.

    """
    num_uniq = len(word_count)
    wrdcnt = word_count.values()
    #print('num uniq', num_uniq)    
    return (num_uniq, wrdcnt)
   
def traverse_rec(path):    
    files = []    
    for entry in os.scandir(path):
        if entry.is_dir():                                  
            files += traverse_rec(entry.path)
        else:
            files.append(entry.path)
    for title in files:
        if title.endswith ('.txt'):
            print(os.path.join(book_dir, title) )
            inputfile = read_book(title)
            (num_uniq, wrdcnt) = word_stats(count_words(inputfile))    
    return files               

def directory_traversal(path):    
    title_num = 1
    for language in os.listdir(book_dir):
        for author in os.listdir(book_dir + '\\'+ language):
            for title in os.listdir(book_dir + '\\'+ language + '\\' + author):
                #inputfile = os.path.join(book_dir,language, author, title)                
                inputfile = book_dir + '\\'+ language + '\\' + author + '\\' +title
                text = read_book(inputfile)
                (num_uniq, wrdcnt) = word_stats(count_words(text))
                stats.loc[title_num] = language, author.capitalize(), title.replace('.txt', ''), sum(wrdcnt), num_uniq
                title_num +=1 
    
stats=pd.DataFrame(columns = ('language', 'author','title', 'length','unique'))

directory_traversal(book_dir)

plt.plot(stats.length, stats.unique, 'bo' )
plt.figure(figsize=(10,10))
subset= stats[stats.language =='English']
plt.loglog(subset.length, subset.unique, 'o', label = 'English', color = 'crimson')
subset= stats[stats.language =='French']
plt.loglog(subset.length, subset.unique, 'o', label = 'French', color = 'forestgreen')
subset= stats[stats.language =='German']
plt.loglog(subset.length, subset.unique, 'o', label = 'German', color = 'orange')
subset= stats[stats.language =='Portuguese']
plt.loglog(subset.length, subset.unique, 'o', label = 'Portuguese', color = 'blueviolet')
plt.legend()
plt.xlabel('Book length')
plt.ylabel('Number of unique words')
plt.savefig('Language frequency.pdf')

