// JS Scripts specially for user edit form template

/*
 * Highlighting date of birth differences
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
 * Highlighting date of birth differences
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
 * Adding datepicker after page reload
 */
$(document).ready(function () {
  $(".datepicker").datepicker({
    dateFormat: "dd.mm.yy",
    changeMonth: true,
    changeYear: true,
    yearRange: "1900:2024",
  });
});
