
function setBubble(range, bubble) {
  const val = range.value;
  const min = range.min ? range.min : 0;
  const max = range.max ? range.max : 100;
  const newVal = Number(((val - min) * 100) / (max - min));
  bubble.innerHTML = val;

  // Sorta magic numbers based on size of the native UI thumb
  bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
}

function checkSelection(){
    var valid = false;
    var moods = document.getElementsByName("mood");
    var genres = document.getElementsByName("genres");

    for (var i=0; i < moods.length; i++){
        console.log(moods[i])
        if (moods[i].checked) {
            valid = true;
            break;
        }
    }
    if (valid) { 
        valid = false;
        for (var i=0; i < genres.length; i++) {
            console.log(genres[i])
            if (genres[i].checked) {
                valid = true;
                break;
            }
        }
    }
    
    if (!valid) {
        alert("Please select one option from each form!");
        return valid;
    }
}

function ckChange(ckType){
    var ckName = document.getElementsByName(ckType.name);
    var checked = document.getElementById(ckType.id);
    
    if (checked.checked) {
      for(var i=0; i < ckName.length; i++){
        console.log(ckName[i]);
        if (!ckName[i].checked || (ckName[i].checked && ckName[i].id != 'surprise me')){
            ckName[i].checked = false;
            ckName[i].disabled = true;
          } else {
            ckName[i].disabled = false;
          }
      } 
    }
    else {
      for(var i=0; i < ckName.length; i++){
        ckName[i].disabled = false;
      } 
    }    
}

