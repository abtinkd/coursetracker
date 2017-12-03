$(document).ready(function () {
	var count = 0;
	
	$('.progress').each(function(){
		
		var datav = $('.progress-bar')[count].style.width;
		datav = datav.replace(/%/g,"");
		count += 1;
		if (datav <= 25)
			$('.progress-bar').css("background", "rgba(255, 0, 0, 1)");
		else if (datav <= 50)
			$('.progress-bar').css("background", "rgba(255, 153, 0, 1)");
		else if (datav <= 75)
			$('.progress-bar').css("background", "rgba(0, 0, 255, 1)");
		else
			$('.progress-bar').css("background", "rgba(0, 255, 0, 1)");
	});
});