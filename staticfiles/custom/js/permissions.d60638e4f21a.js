function selectAll(id, isSelected) {
  var selectObj=document.getElementById(id);
  var options=selectObj.options;
  for(var i=0; i<options.length; i++) {
    options[i].selected=isSelected;
  }
}
