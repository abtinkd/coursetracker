var clock;
var playpause1 = true;

$(document).ready(function () {
    $("#id_course option[value='']").remove();

    clock = $('.clock').FlipClock({
        clockFace: 'HourlyCounter',
        countdown: false,
        autoStart: false
    });

    document.getElementById('playpause').innerText = 'Start';

    // Disable the stop button if start button is available
    $("#stopbutton").hide();

    $('.switch').click(function (e) {
        // Prevent the page from refreshing
        e.preventDefault();

        // Here we toggle playpause from true to false and vice versa
        playpause1 = !playpause1;
        if (playpause1) {
            document.getElementById('playpause').innerText = 'Start';
            clock.stop();
        }
        else {
            // document.getElementById('playpause').innerText = 'Pause Timer';

            // Disable the button after being clicked once
            $("#playpause").hide();

            // Disable the stop button if start button is available
            $("#stopbutton").show();

            clock.start();
            $.ajax({
                url: "", type: "POST",
                data: {
                    start_time: new Date().toISOString(),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                error: function (xhr, textStatus, thrownError) {
                    alert("An error occurred: " + xhr.status + " " + xhr.statusText);
                }
            });
        }
    });


    $("#id_course").change(function () {

        clock = $('.clock').FlipClock({
            clockFace: 'HourlyCounter',
            countdown: false,
            autoStart: false
        });

        document.getElementById('playpause').innerText = 'Start';

        // Enable the button after being clicked once
        $("#playpause").show();

        // Disable the stop button if start button is available
        $("#stopbutton").hide();

        playpause1 = true;
    });
});