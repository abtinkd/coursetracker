// Using https://github.com/AuspeXeu/bootstrap-datetimepicker
$("#id_start_date").on("change.dp", function (e) {
    window.alert('1');
    $('#id_end_date').datetimepicker('setStartDate', e.date.valueOf());
});

$("#id_end_date").on("changeDate", function (e) {  // TODO fix
    window.alert('1');
    $('#id_start_date').datetimepicker('setEndDate', e.date.valueOf());
});
