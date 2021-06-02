# -*- coding: utf-8 -*-
import json
import os
from collections import defaultdict
from collections import OrderedDict
#from fixedordereddict import FixedOrderedDict
import io

#automatically label the json file...
#also useful when you need to update it
#or change the labeling scheme
#or remove it entirely
#you really ought to do this...
#should be able to correctly label:
#only non-trivial nodes (e.g. ignore conditions, comments,
#references, XORs, and leaves
#and should be able to handle a partially (but correctly) labeled json
#by first parsing out the stuff before the first parenthesis if it includes the top classes
#(so the top 2 classes shouldn't change, but check for the first occurrence of a valid
#first class and a valid second class, and the first following '('
#and don't forget to add or remove the final ')' appropriately;
#and remember that the node might have parentheses within it

"""
def dfs(graph, node, visited):
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph,n, visited)
    return visited

visited = dfs(graph1,'A', [])
"""
global data
data = dict()
global labeled_data
labeled_data = dict()


#def edit_dict(dict, old_key, new_key):
#    for key


#does a depth-first-search of both the original json
#and an (initially empty) dictionary containing the labels. Populates the labels
#as it traverses the original json. The labeled dict should be identical except
#the key/values are prepended with labels
#note that graph and labeled_data_parent refer to the same dict!
#Not sure if that's a problem or a good thing...
def dfs(graph, node, labeled_data_parent):
    count = 0
    node_count = 0
    parent_label = node.split('(')[0]
    print("parent: " + parent_label)
    print("node: " + node)
    print("graph: " + str(graph))
    for e in graph[node]:
        print("orig: " + e)
        if e == u'参照' or e == u'コメント' or e == 'XOR' or e == 'note' or e == 'References':
            continue
        #not sure if this means we've reached the end, or
        print("graph[node][e]: " + str(graph[node][e]))
        if type(graph[node][e]) == type(u"string"):
            #dict[key] -> value
            #and dict has a row of keys, each w/1 value
            #so e.g. parent[child_node] -> child_node's child/leaf
            #so e.g, for child_node in parent, child_node gets a label based
            #on the parent?]
            node_count = node_count + 1
            new_key = parent_label + ":" + "c"+str(node_count)+"("+e.split('(')[-1].strip(')')+')'
            print("new: " + new_key)
            labeled_data_parent = OrderedDict([(new_key, v) if k == e else (k, v) for k, v in labeled_data_parent.items()])
            graph = OrderedDict([(new_key, v) if k == e else (k, v) for k, v in graph.items()])
            #labeled_data_parent[new_key] = labeled_data_parent.pop(e)
            #dfs(data[e], labeled_data_parent[e])
        else:
            count = count + 1
            new_key = parent_label + ":" + str(count)+"("+e.split('(')[-1].strip(')')+')'
            print("new: " + new_key)
            labeled_data_parent = OrderedDict([(new_key, v) if k == e else (k, v) for k, v in labeled_data_parent.items()])
            graph = OrderedDict([(new_key, v) if k == e else (k, v) for k, v in graph.items()])
            print("new graph" + str(graph))
            #labeled_data_parent[new_key] = labeled_data_parent.pop(e)
            dfs(graph[node], new_key, labeled_data_parent[new_key])

    
    #return labeled_data

#reverses parents and children,
#e.g., for references, reverses author/title    
def reverse():
    pass
    return
    
def main():
    dataDirPath = ""
    jsonFileName = "benchmark.json"
    outputFileName = "labeled_benchmark.json"
    
    #label_symbols = []

    with io.open(os.path.join(dataDirPath, jsonFileName), "r", encoding="utf-8") as fd:
        data = json.load(fd, object_pairs_hook=OrderedDict)
    
    #for key, val in data.items():
    #    print(key,val)
    
    first = [key for key in data["Category"]]
    #print("firstクラス")
    #print(first)
    second = {}
    for key in first:
        second[key] = [key2 for key2 in data["Category"][key]]
    #print("secondクラス")
    #print(second)

    #print("got here")
    labeled_data = data
    #labeled_data = #data[first] -> second
    for key in data["Category"]:
        #print("got here")
        for key2 in data["Category"][key]:
            dfs(data["Category"][key], key2, labeled_data["Category"][key][key2])
        
    #labeled_data = dfs(data, labeled_data)
    
    with io.open(os.path.join(dataDirPath, outputFileName), "w", encoding='utf8') as g:
        json.dump(labeled_data, g, indent=4, ensure_ascii=False)
        
if __name__ == "__main__":
    main()