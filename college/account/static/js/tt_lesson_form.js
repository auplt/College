$(document).ready(function () {
  $(".datepicker").datepicker({
    dateFormat: "dd.mm.yy",
    changeMonth: true,
    changeYear: true,
    yearRange: "1900:2024",
    firstDay: 1,
  });
});

$(document).ready(function () {
  $("#id_date")
    .datepicker({
      dateFormat: "dd.mm.yy",
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2024",
      firstDay: 1,
    })
    .on("input change", (event) => {
      let dateMas = $("#id_date").val().split(".");
      let dateStr = dateMas[2] + "-" + dateMas[1] + "-" + dateMas[0];
      let dayOfWeek = new Date(Date.parse(dateStr))
        .toLocaleDateString("en", { weekday: "short" })
        .toUpperCase();
      $("#id_day_name").val(dayOfWeek);
    });
});
