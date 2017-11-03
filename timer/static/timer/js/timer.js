var clock;
var d;
var end_time;
var c;
var start_time_day = 0;
var start_time_month = 0;
var start_time_year = 0;
var start_time_hours = 0;
var start_time_minutes = 0;
var start_time_seconds = 0;
var end_time_day = 0;
var end_time_month = 0;
var end_time_year = 0;
var end_time_hours = 0;
var end_time_minutes = 0;
var end_time_seconds = 0;

var playpause1 = true;

$(document).ready(function() {
	
	// alert("DOM ready.");	
	$("#id_course option[value='']").remove();
	
	clock = $('.clock').FlipClock({
		clockFace: 'HourlyCounter',
		countdown: false,
		autoStart: false
	});
	
	document.getElementById('playpause').innerText = 'Start Timer';
	
	
	
	$('.switch').click(function(e) {
		// Here we toggle playpause from true to false and vice versa
		playpause1 = !playpause1;
		// alert("1st " + playpause1);
		if(playpause1)
		{
			document.getElementById('playpause').innerText = 'Start Timer';
			clock.stop();
			d = new Date();
			end_time_day = d.getDate();
			// alert(end_time_day);
			end_time_month = d.getMonth() + 1;
			// alert(end_time_month);
			end_time_year = d.getFullYear();
			// alert(end_time_year);
			end_time_hours = d.getHours();
			// alert(end_time_hours);
			end_time_minutes = d.getMinutes();
			// alert(end_time_minutes);
			end_time_seconds = d.getSeconds();
			// alert(end_time_seconds);
		}
		else
		{
			document.getElementById('playpause').innerText = 'Stop Timer';
			clock.start();
			c = new Date();
			start_time_day = c.getDate();
			// alert(start_time_day);
			start_time_month = c.getMonth() + 1;
			// alert(start_time_month);
			start_time_year = c.getFullYear();
			// alert(start_time_year);
			start_time_hours = c.getHours();
			// alert(start_time_hours);
			start_time_minutes = c.getMinutes();
			// alert(start_time_minutes);
			start_time_seconds = c.getSeconds();
			// alert(start_time_seconds);
		}
	});
	
	
	
	$("#id_course").change(function(){
		
		clock = $('.clock').FlipClock({
			clockFace: 'HourlyCounter',
			countdown: false,
			autoStart: false
		});		
		
		document.getElementById('playpause').innerText = 'Start Timer';		
		playpause1 = true;	
    });
});