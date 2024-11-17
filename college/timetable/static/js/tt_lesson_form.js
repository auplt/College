// JS Scripts specially for lesson timetable form template

/*
 * Adding datepicker
 */
$(document).ready(function () {
  $(".datepicker").datepicker({
    dateFormat: "dd.mm.yy",
    changeMonth: true,
    changeYear: true,
    yearRange: "1900:2100",
    firstDay: 1,
  });
});
