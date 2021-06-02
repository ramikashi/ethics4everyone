#!/usr/bin/python

import json
import math
from www.template import canvas

class JsonGenerator:
    def __init__(self, jsonFileName):
        self.nodes = set()
        self.nodeDesc = {}
        self.nodeProps = {}
        self.nodeColor = {}
        self.nodeShape = {}
        self.edges = set()
        self.jsonFileName = jsonFileName

        self.DEFAULT_COLOR    = '#283747'
        self.TBD_DEMANDS_COLOR        = '#ff00ff'
        self.PERMITS_COLOR    = '#00ff00'
        self.PROHIBITS_COLOR = '#ff0000'
        self.DEMANDS_COLOR    = '#00bbc3'
        self.REF_COLOR = '#4b0082'
        self.XOR_COLOR = '#8b4513'
        self.TBD_PROHIBITS_COLOR = '#ffa500'
        
        self.CONSENT_BORDER_COLOR = '#00ff00'#border-color #for nodes involving consent

        self.DEFAULT_SHAPE = 'ellipse'
        self.CONDITION_SHAPE = 'star'
        #self.REFERENT_SHAPE = 'star'#most immediate referent
        self.XOR_SHAPE = 'triangle'
        self.REF_SHAPE = 'square'     

        self.code1 = canvas.code1
        self.code2 = canvas.code2
        self.code3 = canvas.code3
        
        #set to show references!
        self.show_refs = True

    """https://js.cytoscape.org/#style
    Uses cytoscape styling rules via json to built a json string
    Adjusts the string as necessary given certain metadata.
    Note that this is not a per-node string, but all the nodes in 
    the graph (or at least in the current subtree).
    The string is merely appended to as it is built
    """
    def genCode(self):
        ret = ""
        ret += self.code1
        for n in self.nodes:
            ret += '{ data: { id: "%s", name: "%s", shape: "%s"},\n style: { "background-color": "%s"} },\n' % (n, self.nodeDesc[n], self.nodeShape[n], self.nodeColor[n])
            if "Consentable" in self.nodeProps[n]:
                ret = ret[0:-5]+', "border-width": 4, "border-color": "%s"} },\n' % (self.CONSENT_BORDER_COLOR)
            if "Internally_Motivated" in self.nodeProps[n]:
                ret = ret[0:-5]+', "width":"4em", "height":"4em"} },\n'
        ret += self.code2
        for e in self.edges:
            ret += '{ data: { source: "%s", target: "%s" } },' % (e[0], e[1])
        ret += self.code3
        return ret
    
    """Wtf does this do??"""
    """
    the first call to this will be with parentName=""
    and desc=secondCategory, e.g. "Vulnerability Research"
    where desc is the edge's value (i.e. its description)'
    """
    def addNode(self, parentName="", desc=""):
        #if it's an XOR or Properties node, you don't add it
        #as an edge, so it shouldn't show up in the graph
        #and or desc == "Condition" shouldn't be necessary if 
        #it only shows up in a list
        if desc == "XOR" or desc == "Properties":# or type(desc) == type([]):
            nodeName = parentName
            if desc == "XOR":
                self.nodeShape[nodeName] = self.XOR_SHAPE
                self.nodeColor[nodeName] = self.XOR_COLOR
            #if desc == "Properties":
            #    self.nodeShape[nodeName] = self.CONDITION_SHAPE
            ##if type(desc) == type([]):
            ##    if "Condition" in desc:
            ##        self.nodeShape[nodeName] = self.CONDITION_SHAPE
        else:
            #terrible format string giving an up to 3 digit id to 
            #the node based on...the current number of nodes, since you start with 0,
            #and add a node each time. So first it'll be 0, and then you'll
            #add the first node after assigning it a nodeName of 0,
            #and then the second node will get a nodeName of 1 since 1 node already exists
            nodeName = "n%03d" % len(self.nodes) 
            print(nodeName)
            self.nodes.add(nodeName)
            self.nodeProps[nodeName] = set() #initialize node properties...hopefully it's not already initialized
            if desc == "参照" or desc == "References":
                self.nodeColor[nodeName] = self.REF_COLOR
                self.nodeShape[nodeName] = self.REF_SHAPE
            else:
                self.nodeColor[nodeName] = self.DEFAULT_COLOR
                self.nodeShape[nodeName] = self.DEFAULT_SHAPE
            if parentName != "":
                self.edges.add((parentName, nodeName))
            #why not just condense the below 3 lines 
            #into self.nodeDesc[nodeName] = desc ?
            self.nodeDesc[nodeName] = ""
            if desc != "":
                self.nodeDesc[nodeName] = desc
        return nodeName

    def line_splitter(self, text):
        """
        splits the given text up if it's in Japanese.
        Otherwise, just returns the text because it doesn't need to be split.
        Basically a hack to auto-wrap text (since Japanese has no spaces),
        but ignore if it is English
        
        WARNING: need to type check and skip if it's not a string, since you
        might have e.g. lists being passed into this
        """
        min_len = 30
        wrap_cutoff = min_len - 5
        if type(text) == type(u"string") and len(text) >= min_len and self.jsonFileName == "benchmark.json":
            #(The Japanese versions should be called benchmark.json)
            num = math.ceil(len(text) / min_len)
            newlined_data = text[0:wrap_cutoff]
            for i in range(1,num):
                newlined_data = newlined_data[0:i*wrap_cutoff] + '\\n' + text[i*wrap_cutoff:]
            #might cause a bug if tmpParentName is expected to
            #be the same as e (edj/edge/key), or something
            return newlined_data
        else:
            return text
    
    """
    dict data is the current subtree that will have a node created for it and 
    whose keys will be iterated over to find leaves/the next subtree
    string parentName, the tree that data is an item/child of
    string desc probably the actual text of the head node/label of data,
    since data is really outlined like this:
    "desc":{data_edge1:val1, data_edge2:val2}
    ...I think
    """
    def dfs(self, data, parentName="", desc=""):
        print(len(desc)) #desc == descendent? description?
        print(len(parentName))
        nodeName = self.addNode(parentName, self.line_splitter(desc))
        #if the data is a dictionary
        if type(data) == type({}):
            if "note" in data:
                del data["note"]
            if "コメント" in data:
                del data["コメント"]
            #if "Condition" in data:
            #    del data["Condition"]
            #    self.nodeShape[tmpParentName] = self.CONDITION_SHAPE

            if not self.show_refs:
                if "参照" in data:
                    del data["参照"]
                if "References" in data:
                    del data["References"]
                
            #for leaf nodes. I think edj is just an edge/key (left side) in the current subtree
            for edj in data:
                #if the value of the edge node is a string, it's a leaf
                if type(data[edj]) == type(u"string"):
                    tmpParentName = self.addNode(nodeName, self.line_splitter(edj))
                    leafName = self.addNode(tmpParentName, self.line_splitter(data[edj]))
                    if data[edj] == "Demands" or data[edj] == "必須":
                        self.nodeColor[leafName] = self.DEMANDS_COLOR
                        self.nodeColor[tmpParentName] = self.DEMANDS_COLOR
                    elif data[edj] == "Permits" or data[edj] == "非倫理的ではない":
                        self.nodeColor[leafName] = self.PERMITS_COLOR
                        self.nodeColor[tmpParentName] = self.PERMITS_COLOR
                    elif data[edj] == "Prohibits" or data[edj] == "禁止":
                        self.nodeColor[leafName] = self.PROHIBITS_COLOR
                        self.nodeColor[tmpParentName] = self.PROHIBITS_COLOR
                    elif data[edj] == "TBD":
                        self.nodeColor[leafName] = self.TBD_COLOR
                        self.nodeColor[tmpParentName] = self.TBD_COLOR
                    elif data[edj] == "Recommended" or data[edj] == "必須の可能性がある":
                        self.nodeColor[leafName] = self.TBD_DEMANDS_COLOR
                        self.nodeColor[tmpParentName] = self.TBD_DEMANDS_COLOR
                    elif data[edj] == "Grey" or data[edj] == "グレー":
                        self.nodeColor[leafName] = self.TBD_PROHIBITS_COLOR
                        self.nodeColor[tmpParentName] = self.TBD_PROHIBITS_COLOR
                    #node name is the parent node
                    elif self.nodeColor[nodeName] == self.REF_COLOR:
                        #leafname is the leaf/right side
                        self.nodeColor[leafName] = self.REF_COLOR
                        #tmpParentName is the left side of the node
                        self.nodeColor[tmpParentName] = self.REF_COLOR
                    #if data[edj] == "Condition":
                        #self.nodeShape[nodeName] = self.CONDITION_SHAPE
                        #but this is redundant...and so are the XOR/REF color things...?
                        #continue
                    elif edj == "XOR":
                        self.nodeColor[leafName] = self.XOR_COLOR
                #if the node is like "Properties":["Condition","Consent"]
                elif type(data[edj]) == type([]):
                    if "Condition" in data[edj]:
                        self.nodeShape[nodeName] = self.CONDITION_SHAPE
                        self.nodeProps[nodeName].add("Internally_Motivated")
                    if "Consent" in data[edj]:
                        self.nodeProps[nodeName].add("Consentable")
                #otherwise, it's probably another nested dictionary        
                #so just search that dictionary, and pass in
                #the current data node name as its parent,
                #since we're searching each of that node's children in this loop
                #And then pass in this edge's key as the description
                else:
                    self.dfs(data[edj], nodeName, self.line_splitter(edj))
        #if the data is a list, such as when...it's a note that isn't deleted?
        #I feel like I can delete this...
        elif type(data) == type([]):
            for edj in data:
                print(edj)
                self.dfs(edj, nodeName)