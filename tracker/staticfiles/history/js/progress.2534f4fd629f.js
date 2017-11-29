 $(document).ready(function () {
	 
	var count = 0;
	
	$('.progress').each(function(){
		
		var datav = $('.progress-bar')[count].style.width;
		datav = datav.replace(/%/g,"");
		// alert(datav);
		count = count + 1;
		
		var dataval = datav;
		
		if (dataval <= 25) {
			$('.progress-bar').css("background", "rgba(255, 0, 0, 1)");
			// $('.progress-bar').css("background", "rgba(0, 0, 0, 1)");
			// $('.progress-bar').css("background", "-webkit-linear-gradient(top, rgba(255, 0, 0, 1) 0%, rgba(0, 0, 0, 1) 100%)");
			// $('.progress-bar').css("background", "linear-gradient(to bottom, rgba(255, 0, 0, 1) 0%, rgba(0, 0, 0, 1) 100%)");
		}
		else if (dataval > 25 && dataval <= 50) {
			$('.progress-bar').css("background", "rgba(255, 153, 0, 1)");
			// $('.progress-bar').css("background", "rgba(0, 0, 0, 1)");
			// $('.progress-bar').css("background", "-webkit-linear-gradient(top, rgba(0, 0, 255, 1) 0%, rgba(0, 0, 0, 1) 100%)");
			// $('.progress-bar').css("background", "linear-gradient(to bottom, rgba(0, 0, 255, 1) 0%, rgba(0, 0, 0, 1) 100%)");
		}
		else if (dataval > 50 && dataval <= 75) {
			$('.progress-bar').css("background", "rgba(0, 0, 255, 1)");
			// $('.progress-bar').css("background", "rgba(0, 0, 0, 1)");
			// $('.progress-bar').css("background", "-webkit-linear-gradient(top, rgba(255, 255, 0, 1) 0%, rgba(0, 0, 0, 1) 100%)");
			// $('.progress-bar').css("background", "linear-gradient(to bottom, rgba(255, 255, 0, 1) 0%, rgba(0, 0, 0, 1) 100%)");
		}
		else if (dataval > 75) {
			$('.progress-bar').css("background", "rgba(0, 255, 0, 1)");
			// $('.progress-bar').css("background", "rgba(0, 0, 0, 1)");
			// $('.progress-bar').css("background", "-webkit-linear-gradient(top, rgba(0, 255, 0, 1) 0%, rgba(0, 0, 0, 1) 100%)");
			// $('.progress-bar').css("background", "linear-gradient(to bottom, rgba(0, 255, 0, 1) 0%, rgba(0, 0, 0, 1) 100%)");
		}
	});
});