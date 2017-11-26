 $(document).ready(function () {
    var dataval = parseInt($('.progress').attr("data-amount"));
    if (dataval < 100) {
        $('.progress .amount').css("width", 100 - dataval + "%");
    }

  /*FOR DEMO ONLY*/
    $('#increase').click(function () {
        modifyProgressVal(1);
    });
    $('#decrease').click(function () {
        modifyProgressVal(-1);
    });
    function modifyProgressVal(type) {
        dataval = parseInt($('.progress').attr("data-amount"));
        if (type == 1) dataval = Math.min(100,dataval + 10)
        else if (type == -1) dataval = Math.max(0,dataval - 10);
        $('.progress .amount').css("width", 100 - dataval + "%");
		if (dataval > 50) alert("Success");
        $('.progress').attr("data-amount", dataval);
    }
});