$("#start_date").on("dp.change", function (e) {
    $('#end_date').data("DateTimePicker").minDate(e.date);
});

$("#end_date").on("dp.change", function (e) {  // TODO fix
    $('#start_date').data("DateTimePicker").maxDate(e.date);
});