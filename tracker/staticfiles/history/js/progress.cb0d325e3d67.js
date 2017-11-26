// var progressBarColor;

// var someValueToCheck = 5;

// if(someValueToCheck >= 10) progressBarColor = "#A52A2A";
// else if(someValueToCheck >=5) progressBarColor = "#00FFFF";
// else progressBarColor = "#00008B";

// $("#progressbar").css('background-color', progressBarColor);


function move() {
  var elem = document.getElementById("myBar");   
  var width = 1;
  var id = setInterval(frame, 10);
  function frame() {
    if (width >= 100) {
      clearInterval(id);
    } else {
      width++; 
      elem.style.width = width + '%'; 
    }
  }
}
