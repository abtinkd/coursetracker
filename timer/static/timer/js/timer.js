$(document).ready(function () {
    var paused = true;
    var timer = $('.timer').FlipClock({
        clockFace: 'HourlyCounter',
        countdown: false,
        autoStart: false
    });

    $("#id_course option[value='']").remove();
    document.getElementById('startbutton').innerText = 'Start';
    $("#stopbutton").hide();

    $('.switch').click(function (e) {
        e.preventDefault();  // prevent the page from refreshing

        if (!paused) {
            document.getElementById('startbutton').innerText = 'Start';
            timer.stop();
        } else {
            $("#startbutton").hide();
            $("#stopbutton").show();

            timer.start();
            $.ajax({url: "", type: "POST", data: {start_time: new Date().toISOString(),
                                                  csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()}});
        }

        paused = !paused;
    });
});