#!/usr/bin/python3

from flask import Flask, request, send_from_directory, render_template
#import getJson
import www.graph as graphmod

app = Flask(__name__, static_url_path='')
graph = graphmod.Graph()

@app.route('/')
def root():
    """
    The main, Japanese tree
    """
    global graph
    graph = graphmod.Graph()
    #also at some point need to change the selected menus to correspond to the old ones?
    #newLanguageKeys() #(also need firstCategory and secondCategory to be global)
    #and need to call both changeList2() and getGraphScript()
    with open('./template/index.html', "r") as fd:
        return fd.read()
        
@app.route('/eng')
def eng_root():
    """
    The alternate, English tree
    """
    global graph
    graph = graphmod.Graph(jsonFileName = "eng_labeled_benchmark.json")
    #also at some point need to change the selected menus to correspond to the old ones?
    #newLanguageKeys() #(also need firstCategory and secondCategory to be global)
    #and need to call both changeList2() and getGraphScript()
    with open('./template/index_eng.html', "r") as fd:
        return fd.read()
        
@app.route('/info')
def pdf_info():
    return send_from_directory('./data/', 'CSS2018 ethics KB proposal r2.pdf')
    
@app.route('/raw')
def raw_data():
    return send_from_directory('./data/', 'benchmark.json')

@app.route('/raw_eng')
def eng_data():
    return send_from_directory('./data/', 'eng_labeled_benchmark.json')
    
@app.route('/static/js/<path:path>')
def returnStaticJS(path):
    return send_from_directory('./static/js/', path)

@app.route('/static/css/<path:path>')
def returnStaticCSS(path):
    return send_from_directory('./static/css/', path)

@app.route("/api/graphScript/<key1>/<key2>")
def getGraphScript(key1, key2):
    return graph.retGraphScript(key1, key2)

@app.route("/api/category")
def getFirstCategory():
    firstCategory = graph.retFirstCategory()
    return firstCategory

@app.route("/api/category/<key1>")
def getSecondCategory(key1):
    secondCategory = graph.retSecondCategory(key1)
    return secondCategory

"""
def newLanguageKeys():
    new_firstCategory, new_secondCategory = graph.switchLanguage(self, firstCategory, secondCategory)
    global firstCategory
    global secondCategory
    firstCategory = new_firstCategory
    secondCategory = new_secondCategory
"""
    
#app.debug = True; #BUG!adding a proceses=2 parameter or w/e makes only the Japanese version display.  TODO! fix
app.run(host="0.0.0.0")


