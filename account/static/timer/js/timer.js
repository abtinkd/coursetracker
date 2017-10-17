var clock;
		
$(document).ready(function() {
			
	clock = $('.clock').FlipClock({
		clockFace: 'DailyCounter',
		countdown: false
	});
	
	$('.stop').click(function(e) {

		clock.stop();
	});
});