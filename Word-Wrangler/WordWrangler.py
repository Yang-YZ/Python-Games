"""
Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if len(list1) == 0:
        return []
    list_out = [list1[0]]
    for item in list1:
        if item != list_out[len(list_out)-1]:
            list_out.append(item)
    return list_out

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersect_list = []
    index1 = 0
    index2 = 0
    while index1 < len(list1) and index2 < len(list2):
            item1 = list1[index1]
            item2 = list2[index2]
            if type(item1) != int:
                item1 = ord(list1[index1])
            if type(item2) != int:
                item2 = ord(list2[index2])
            if item1 == item2:
                intersect_list.append(list1[index1])
                index1 += 1
                index2 += 1
            elif item1 < item2:
                index1 += 1
            else:
                index2 += 1
#	for item in list1:
#        if item in list2 and item not in intersect_list:
#            intersect_list.append(item)
    return intersect_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    merge_list = []
    index1 = 0
    index2 = 0
    while index1 < len(list1) and index2 < len(list2):
            item1 = list1[index1]
            item2 = list2[index2]
            if type(item1) != int:
                item1 = ord(list1[index1])
            if type(item2) != int:
                item2 = ord(list2[index2])
#            if item1 == item2:
#                merge_list.append(list1[index1])
#                index1 += 1
#                index2 += 1
            if item1 <= item2:
                merge_list.append(list1[index1])
                index1 += 1
            else:
                merge_list.append(list2[index2])
                index2 += 1
    if index1 < len(list1):
        merge_list.extend(list1[index1:])
    if index2 < len(list2):
        merge_list.extend(list2[index2:])
    return merge_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1

    middle = len(list1)/2
    left = merge_sort(list1[:middle])
    right = merge_sort(list1[middle:])

    return merge(left, right)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == "":
        return [""]
    first = word[0]
    rest = word[1:]
    if first == "":
        return [""]
    elif rest == "":
        return ["", first]
    
    rest_strings = gen_all_strings(rest)
    new_strings = []
    for string in rest_strings:        
        new_string = ""
        for str_idx in range(len(string) + 1):
            new_string = string[:str_idx] + str(first) + string[str_idx:]
            new_strings.append(new_string)
    new_strings.extend(rest_strings)
    return new_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    data = []
    for line in netfile.readlines():
        data.append(str(line))
    return data

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()
print gen_all_strings('')
print remove_duplicates([])