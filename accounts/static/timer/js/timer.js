var clock;

$(document).ready(function() {

	// alert("DOM ready.");
	$("#id_course option[value='']").remove();

	clock = $('.clock').FlipClock( {
		clockFace: 'HourlyCounter',
		countdown: false,
		autoStart: true
	});
});