# -*- coding:utf-8 -*-

code1 = """
var cy = window.cy = cytoscape({
    container: document.getElementById('cy'),
    zoom: 0.1,
    wheelSensitivity: .20,
    minZoom: 1e-1,
    maxZoom: 5,
    
    boxSelectionEnabled: false,
    autounselectify: true,

    layout: {
        name: 'dagre',
        rankDir: 'LR'
    },

    style: [
        {
            selector: 'node',
            style: {
                'content': 'data(name)',
                'text-opacity': 0.8,
                'font-size': 42.0,
                'text-valign': 'bottom',
                'text-halign': 'right',
                'text-wrap': 'wrap',
                'text-max-width': '750px',
                'background-color': 'data(color)',
                'shape': 'data(shape)'
            }
        },
        
        {
            selector: ':parent',
            style: {
                'background-opacity': 0.333
            }
        },

        {
            selector: "node.cy-expand-collapse-collapsed-node",
            style: {
                "background-color": "darkblue",
                "shape": "rectangle"
            }
        },

        {
            selector: 'edge.meta',
            style: {
                'width': 2,
                'line-color': 'red'
            }
        },

        {
            selector: ':selected',
            style: {
                "border-width": 3,
                "border-color": '#DAA520'
            }
        },

        {
            selector: 'edge',
            style: {
                'width': 4,
                'target-arrow-shape': 'triangle',
                'line-color': '#808b96',
                'target-arrow-color': '#808b96'
            }
        }
    ],

    elements: {
        nodes: [
"""

code2 = """
],
edges: [
"""


code3 = """
        ]
    },
});
document.getElementById('cy').style.height = '89%';
cy.resize();
cy.fit();
cy.expandCollapse({
    layoutBy: {
        name: "dagre",
        animate: "end",
        randomize: false,
        fit: true
    },
    fisheye: true,
    animate: true
});

for (i=0;i<cy.elements().nodes().length;i++){
    var elem = cy.getElementById(cy.elements().nodes()[i].data().id);
    var tippy_data = cy.elements().nodes()[i].data().name;
    tippies.push(makeTippy(elem, tippy_data));
    };
    

//hotfix??
//for (const popper of document.querySelectorAll('.tippy-popper')) {
//    popper.parentNode.removeChild(popper);
//  }
//or maybe:
//for (const instance of tippies){
//  instance.destroy()
//}
"""

