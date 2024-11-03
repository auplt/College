// JS Scripts specially for lesson time form template

/*
 * Additng timepicker for form's time input fields
 */
$(document).ready(function () {
  $(".timepicker").timepicker({
    controlType: "select",
    oneLine: true,
    timeInput: true,
    timeFormat: "HH:mm",
    hourMin: 8,
    hourMax: 21,
    stepMinute: 5,
  });
});
