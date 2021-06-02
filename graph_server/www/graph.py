#!/usr/bin/pyhton

import os
import json
from www.jsonGen import JsonGenerator

class Graph:
    def __init__(self, dataDirPath = "data", jsonFileName = "benchmark.json"):
        if jsonFileName == "benchmark.json" or jsonFileName == "eng_labeled_benchmark.json":
            self.jsonFileName = jsonFileName
            with open(os.path.join(dataDirPath, jsonFileName), "r") as fd:
                self.data = json.load(fd)
            self.firstCategories = [key for key in self.data["Category"]]
            self.secondCategories = {}
            for key in self.firstCategories:
                self.secondCategories[key] = [key2 for key2 in self.data["Category"][key] if not key2 == "コメント" and not key2 == "note" and not key2 =="Properties"]
                
    """
    def switchLanguage(self, firstCategory, secondCategory):
        #extract the key from the categories
        #search the language (later you might have a language variable) trees for those keys and get the categories
        #return the corresponding categories
    """

    def retFirstCategory(self):
        return json.dumps(self.firstCategories)

    def retSecondCategory(self, firstCategory):
        return json.dumps(self.secondCategories[firstCategory])

    def retGraphScript(self, firstCategory, secondCategory):
        jg = JsonGenerator(self.jsonFileName)
        jg.dfs(self.data["Category"][firstCategory][secondCategory], desc=secondCategory)
        return jg.genCode()


    
