# -*- coding: utf-8 -*-
import json
import os
from collections import defaultdict
from collections import OrderedDict
import io
import sys
import re

#automatically label the json file...
#also useful when you need to update it
#or change the labeling scheme
#or remove it entirely
#should be able to correctly label:
#only non-trivial nodes (e.g. ignore conditions, comments,
#references, XORs, and leaves
#and should be able to handle a partially (but correctly) labeled json
#by first parsing out the stuff before the first parenthesis if it includes the top classes
#(so the top 2 classes shouldn't change, but check for the first occurrence of a valid
#first class and a valid second class, and the first following '('
#and don't forget to add or remove the final ')' appropriately;
#and remember that the node might have parentheses within it

if sys.version_info[0:2] != (3,6):
    raise Exception("Python 3.6 is required (for using ordered dictionaries to traverse the json)")
    exit()

global data
data = dict()
global ordered_data
ordered_data = OrderedDict() 
global labeled_data
labeled_data = dict()

def change(parent_label, count, e, cond=False):
    """
    string parent_label label of the parent; carried on to the child/leaf
    int count the number of the current node relative to its siblings
    string e the original label of the node
    bool cond whether this is a final condition or a parent/activity description
    
    
    returns a string used to replace the key/label
    Change this method to change the labeling scheme or remove it.
    WARNING: removing the labeling scheme entirely requires you to relabel at
    least the first 2 levels (e.g. PR and PR:PD) if you want to add labels
    again. For that purpose, consider keeping a copy with no labels except
    for the first two levels
    """
    parent_prefix = parent_label.split('(')[0].strip(')')
    prefix = e.split('(')[0].strip(')')
    print('prefix: ' + prefix)
    
    #set the default
    clean_e = e
    print('length: ' + str(len(e.split('('))))
    if len(e.split('(')) == 2:
        #in this case, either it has a prefix, or it has extra text.
        #If it has a prefix, get the last item
        #(check if it's a real prefix and not just normal stuff outside parentheses)
        if re.match(r'[A-Z][A-Z](:[A-Z][A-Z])?(:[0-9])*',prefix):
            clean_e = e.split('(')[-1].strip(')')
        #but if it has extra text instead, preserve that
        #else:
        #    clean_e = e
    elif len(e.split('(')) > 2:
        #if it has a prefix, then it has a prefix and other stuff,
        #so strip the prefix only
        #(check if it's a real prefix and not just normal stuff outside parentheses)
        if re.match(r'[A-Z][A-Z](:[A-Z][A-Z])?(:[0-9])*',prefix):
            clean_e = e.lstrip(prefix+'(').strip(')')
        #if it has no prefix, then it's just multiple parenthetical statements,
        #so save the whole thing
    #else:
    #    clean_e = e
    #clean_e = e.split('(')[-1].strip(')')
    print('clean_e: ' + clean_e)
    
    if cond:
        counter = "c"+str(count)
    else:
        counter = str(count)
    
    #change this to change how labeling happens 
    #(e.g. make it blank to remove labels)
    new_label = parent_prefix + ":" + counter + "(" + clean_e + ')'
    return new_label

#does a depth-first-search of both the original json
#and an (initially empty) dictionary containing the labels. Populates the labels
#as it traverses the original json. The labeled dict should be identical except
#the key/values are prepended with labels
def dfs(entry, parent_label, labeled_data_parent):
    """
    graph is an Ordered dict that is not modified, whereas
    labeled_data_parent is a regular dict that is modified
    
    This will label anything that has a parent, according to the parent's
    label. If you don't want the children labeled, don't label the parent.
    """
    count = 0
    node_count = 0
    print("parent: " + parent_label)
    if type(entry) == type(ordered_data) and parent_label:
        for e in entry:
            print("e: " + str(e))
            print("entry[e]: " + str(entry[e]))
            if e == u'参照' or e == u'コメント' or e == 'note' or e == 'References':
                continue
            print("graph[node][e]: " + str(entry[e]))
            if e == 'XOR':
                dfs(entry[e], parent_label, labeled_data_parent[e])
            #not sure if this means we've reached the end, or
            elif type(entry[e]) == type(u"string"):
                #for child_node in parent, child_node gets a label based on parent
                node_count = node_count + 1
                new_key = change(parent_label, node_count, e, cond=True)
                print("new: " + new_key)
                labeled_data_parent[new_key] = labeled_data_parent.pop(e)
            else:
                count = count + 1
                new_key = change(parent_label, count, e)
                print("new: " + new_key)
                labeled_data_parent[new_key] = labeled_data_parent.pop(e)
                dfs(entry[e], new_key, labeled_data_parent[new_key])


#reverses parents and children,
#e.g., for references, reverses author/title    
def reverse():
    pass
    return

def helper(dataDirPath, jsonFileName, outputFileName):
    #open the file twice: once as read-only for keeping track of traversal,
    with io.open(os.path.join(dataDirPath, jsonFileName), "r", encoding="shiftjis") as fd:
        ordered_data = json.load(fd, object_pairs_hook=OrderedDict)
    #and once for writing, so you can populate labels using simple modification
    with io.open(os.path.join(dataDirPath, jsonFileName), "r", encoding="shiftjis") as fd:
        data = json.load(fd)
    
    #goes through the first two levels, since those always exist/have labels
    for key in ordered_data["Category"]:
        for key2 in ordered_data["Category"][key]:
            dfs(ordered_data["Category"][key][key2], key2.split('(')[0], data["Category"][key][key2])

    #you need the indent to pretty-print the json
    with io.open(os.path.join(dataDirPath, outputFileName), "w", encoding='utf8') as g:
        json.dump(data, g, indent=4, ensure_ascii=False)
    
def main():
    dataDirPath = ""
    Ja_jsonFileName = "master-benchmark_updated_translated_v0.90_jp.json"
    Eng_jsonFileName = "master-benchmark_updated_translated_v0.90_eng.json"
    Ja_outputFileName = "ja_labeled_benchmark.json"
    Eng_outputFileName = "eng_labeled_benchmark.json"
    
    helper(dataDirPath, Ja_jsonFileName, Ja_outputFileName)
    helper(dataDirPath, Eng_jsonFileName, Eng_outputFileName)

        
if __name__ == "__main__":
    main()