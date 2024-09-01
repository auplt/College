/*
 * Выделение расхождений в датах рождения
 */
$(document).ready(function () {
  $("#id_tut-date_of_birth")
    .datepicker({
      dateFormat: "dd.mm.yy",
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2024",
    })
    .on("input change", (event) => {
      if (
        $("#id_std-date_of_birth").val() &&
        $("#id_tut-date_of_birth").val() != $("#id_std-date_of_birth").val()
      ) {
        console.log("1");
        $("#id_std-date_of_birth").css("color", "red");
        $("#id_tut-date_of_birth").css("color", "red");
      } else if (
        $("#id_std-date_of_birth").val() == $("#id_std-date_of_birth").val()
      ) {
        $("#id_std-date_of_birth").css("color", "");
        $("#id_tut-date_of_birth").css("color", "");
      }
    });
});
/*
 * Выделение расхождений в датах рождения
 */
$(document).ready(function () {
  $("#id_std-date_of_birth")
    .datepicker({
      dateFormat: "dd.mm.yy",
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2024",
    })
    .on("input change", (event) => {
      if (
        $("#id_tut-date_of_birth").val() &&
        $("#id_tut-date_of_birth").val() != $("#id_std-date_of_birth").val()
      ) {
        console.log("1");
        $("#id_std-date_of_birth").css("color", "red");
        $("#id_tut-date_of_birth").css("color", "red");
      } else if (
        $("#id_tut-date_of_birth").val() == $("#id_std-date_of_birth").val()
      ) {
        $("#id_std-date_of_birth").css("color", "");
        $("#id_tut-date_of_birth").css("color", "");
      }
    });
});
/*
 * Установка datepicker для работы с календарем
 */
$(document).ready(function () {
  $(".datepicker").datepicker({
    dateFormat: "dd.mm.yy",
    changeMonth: true,
    changeYear: true,
    yearRange: "1900:2024",
  });
});
