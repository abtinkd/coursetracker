var progressBarColor;

var someValueToCheck = 5;

if(someValueToCheck >= 10) progressBarColor = "#A52A2A";
else if(someValueToCheck >=5) progressBarColor = "#00FFFF";
else progressBarColor = "#00008B";

$("#progressbar").css('background-color', progressBarColor);