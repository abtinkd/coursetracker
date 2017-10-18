var clock;
var cs;
var course_selected;
var time_interval;
var time_interval1;
var d;
var t;
var c;
var s;
var dict = {};
var playpause1 = true;

$(document).ready(function() {
	
	// alert("DOM ready.");	
	$("#id_course option[value='']").remove();
	
	course_selected = $("#id_course option:selected").text();
	// alert(course_selected);
	
	// Retrieve
	cs  = localStorage.getItem(course_selected);
	alert(course_selected + ", " + cs);
	
	time_interval = 0; //grab the latest time interval from the database for the corresponding course.
	// alert(time_interval1);
	diff = 0;
	
	clock = $('.clock').FlipClock(cs, {
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
			c = new Date();
			s = c.getTime();
			diff = s/1000 - t/1000;
			diff = Math.round(Number(diff));
			cs  = localStorage.getItem(course_selected);
			cs = Math.round(Number(cs));
			alert(diff);
			// time_interval = 0;
			cs = cs + diff;
			alert (cs);
			// alert(time_interval);			
			
			if (typeof(Storage) !== "undefined") {
				// Store
				localStorage.setItem(course_selected, cs);
				// alert(course_selected + ", " + time_interval);
			} else {
				alert("Sorry, your browser does not support Web Storage...");
			}
			cs = 0;
			diff = 0;
			time_interval = 0;			
		}
		else
		{
			document.getElementById('playpause').innerText = 'Stop Timer';
			clock.start();
			d = new Date();
			t = d.getTime();
			// playpause = true;	
		}
	});
	
	
	
	$("#id_course").change(function(){
		
		course_selected = $("#id_course option:selected").text();
		// alert(course_selected);
		
		// Retrieve
		cs2  = localStorage.getItem(course_selected);
		// alert(course_selected + ", " + cs2);
		
		clock = $('.clock').FlipClock(cs2, {
			clockFace: 'HourlyCounter',
			countdown: false,
			autoStart: false
		});		
		
		document.getElementById('playpause').innerText = 'Start Timer';		
		playpause1 = true;	
		diff = 0;
		cs = 0;
		
    });
});