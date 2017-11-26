 $(document).ready(function () {
    var dataval = parseInt($('.progress').attr("style").width);
    if (dataval < 100) {
        $('.progress .amount').css("width", 100 - dataval + "%");
    }
	
	modifyProgressVal(0);
	
	/*FOR DEMO ONLY*/
    // $('#increase').click(function () {
        // modifyProgressVal(1);
    // });
    // $('#decrease').click(function () {
        // modifyProgressVal(-1);
    // });
	
    function modifyProgressVal(type) {
        dataval = parseInt($('.progress').attr("style").width);
        // if (type == 1) dataval = Math.min(100,dataval + 10)
        // else if (type == -1) dataval = Math.max(0,dataval - 10);
        $('.progress .amount').css("width", 100 - dataval + "%");
		if (dataval > 0 && dataval <= 25) {
			$('.progress').css("background", "rgba(0, 0, 0, 1)");
			$('.progress').css("background", "-webkit-linear-gradient(top, rgba(255, 0, 0, 1) 0%, rgba(0, 0, 0, 1) 100%)");
			$('.progress').css("background", "linear-gradient(to bottom, rgba(255, 0, 0, 1) 0%, rgba(0, 0, 0, 1) 100%)");
		}
		else if (dataval > 25 && dataval <= 50) {
			$('.progress').css("background", "rgba(0, 0, 0, 1)");
			$('.progress').css("background", "-webkit-linear-gradient(top, rgba(0, 0, 255, 1) 0%, rgba(0, 0, 0, 1) 100%)");
			$('.progress').css("background", "linear-gradient(to bottom, rgba(0, 0, 255, 1) 0%, rgba(0, 0, 0, 1) 100%)");
		}
		else if (dataval > 50 && dataval <= 75) {
			$('.progress').css("background", "rgba(0, 0, 0, 1)");
			$('.progress').css("background", "-webkit-linear-gradient(top, rgba(255, 255, 0, 1) 0%, rgba(0, 0, 0, 1) 100%)");
			$('.progress').css("background", "linear-gradient(to bottom, rgba(255, 255, 0, 1) 0%, rgba(0, 0, 0, 1) 100%)");
		}
		else if (dataval > 75 && dataval <= 100) {
			$('.progress').css("background", "rgba(0, 0, 0, 1)");
			$('.progress').css("background", "-webkit-linear-gradient(top, rgba(0, 255, 0, 1) 0%, rgba(0, 0, 0, 1) 100%)");
			$('.progress').css("background", "linear-gradient(to bottom, rgba(0, 255, 0, 1) 0%, rgba(0, 0, 0, 1) 100%)");
		}
        $('.progress').attr("data-amount", dataval);
    }
});