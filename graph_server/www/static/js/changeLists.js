function initList()
{
   var list1 = document.getElementById("list1");

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = checkReadyState;
    xmlHttp.open("GET", "api/category", false);
    xmlHttp.send(null);

    function checkReadyState(){
	var result = document.getElementById('JsonScript');
	if ((xmlHttp.readyState == 4) && (xmlHttp.status == 200)){
	    var list = JSON.parse(xmlHttp.responseText);
	    
        //is this useless?
        var option = document.createElement('option');
	    option.text = option.value = list[i];
	    list1.add(option, 0);
	    for (var i = list1.length; i > 0; i--) {
		list1.remove(0);
	    }
        ////
        //create default
        var option = document.createElement('option');
        option.value = option.disabled　= option.selected = '';
		option.text = 'クラス';
        option.style="display:none;";
        list1.add(option, 0);
	    for(var i = 0; i < list.length; i++){
		var option = document.createElement('option');
		option.text = option.value = list[i];
		list1.add(option, 0);
	    }
	}
    }
}

function changeList2()
{
    var list1val = document.getElementById("list1").value;
    var list2 = document.getElementById("list2");

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = checkReadyState;
    xmlHttp.open("GET", "api/category/"+list1val, false);
    xmlHttp.send(null);

    function checkReadyState(){
	var result = document.getElementById('JsonScript');
	if ((xmlHttp.readyState == 4) && (xmlHttp.status == 200)){
	    var list = JSON.parse(xmlHttp.responseText);
	    var option = document.createElement('option');
	    option.text = option.value = list[i];
	    list2.add(option, 0);
	    for (var i = list2.length; i > 0; i--) {
		list2.remove(0);
	    }
        //create default
        var option = document.createElement('option');
        option.value = option.disabled　= option.selected = '';
		option.text = 'サブクラス';
        option.style="display:none;";
        list2.add(option, 0);
        ////
	    for(var i = 0; i < list.length; i++){
		var option = document.createElement('option');
		option.text = option.value = list[i];
		list2.add(option, 0);
	    }
	}
    }
}

function updateTooltips(){
    //destroying the tippies causes an error because it
    //apparently tries to use the tippies after this point...
    //but I guess it's no big deal...
    for (const instance of tippies){
      instance.destroy();
    }
    
}

function getGraphScript(){
    var list1val = document.getElementById("list1").value;
    var list2val = document.getElementById("list2").value;

    updateTooltips();
    
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = checkReadyState;
    xmlHttp.open("GET", "api/graphScript/"+list1val+"/"+list2val, false);
    xmlHttp.send(null);

    function checkReadyState(){
	var result = document.getElementById('graphScript');
	if ((xmlHttp.readyState == 4) && (xmlHttp.status == 200)){
	    eval(xmlHttp.responseText);
	}
    }
}

// init
var tippies = [];
initList();
