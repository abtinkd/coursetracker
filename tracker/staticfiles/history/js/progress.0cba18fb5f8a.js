var bar = document.getElementById("myProgress");
var progress = 0;


function setProgress(percent){
    bar.style.width = percent + "%";

    if (percent > 90)
        bar.className = "bar bar-success";
    else if (percent > 50)
        bar.className = "bar bar-warning";
}

var interval = setInterval(
    function(){
        setProgress(++progress);
        if (progress == 100) window.clearInterval(interval);
    }, 100);