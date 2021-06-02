var makeTippy = function(node, text){
    let tippy1 = tippy( node.popperRef(), {
        html: (function(){
            var div = document.createElement('div');

            div.innerHTML = text;

            return div;
        })(),
        trigger: 'manual',
        placement: 'top',
        interactive: true,
        hideOnClick: false,
        multiple: true,
        dynamicTitle: false,
        sticky: true
    } ).tooltips[0];
    let handler_open = function(){
        node.removeListener('tap', handler_open)
        node.on('tap', handler_close)
        return tippy1.show();
    };
    let handler_close = function(){
        node.removeListener('tap', handler_close)
        node.on('tap', handler_open)
        return tippy1.hide();
    };
    node.on('tap', handler_open);
    //node.on('tap', () => tippy1.show());
    //minimum configs that work: 1) hideOnClick: true/false, node.on mouseover/mouseout
    //with trigger as mouseenter focus. 2) trigger click/manual, 
    //hideonclick false, node.on tap (no hide needed?)
    return tippy1;
};