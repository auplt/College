// JS Scripts specially for user form template

/*
 * Display / hide additional student information
 */
$(document).ready(function () {
  let studentInfo = $(".more_info__student");
  studentInfo.hide();
  let items = $("form p").length - 2;
  $("#id_is_student")[0].addEventListener("change", (event) => {
    if (event.target.checked) {
      studentInfo.show();
      $("#id_std-date_of_birth").prop("required", true);
      if ($("#id_tut-date_of_birth").val()) {
        $("#id_std-date_of_birth").val($("#id_tut-date_of_birth").val());
      }
    } else {
      studentInfo.hide();
      $("#id_std-date_of_birth").prop("required", false);
    }
  });
});

/*
 * Display / hide additional tutor information
 */
$(document).ready(function () {
  let tutorInfo = $(".more_info__tutor");
  tutorInfo.hide();
  let items = $("form p").length;
  $("#id_is_tutor")[0].addEventListener("change", (event) => {
    if (event.target.checked) {
      tutorInfo.show();
      $("#id_tut-date_of_birth").prop("required", true);
      if ($("#id_std-date_of_birth").val()) {
        $("#id_tut-date_of_birth").val($("#id_std-date_of_birth").val());
      }
    } else {
      $("#id_tut-date_of_birth").prop("required", false);
      tutorInfo.hide();
    }
  });
});

/*
 * Display / hide additional information after reloading submited form
 * with errors
 */
$(document).ready(function () {
  if ($("#id_std-date_of_birth").val()) {
    $(".more_info__student").show();
    $("#id_is_student").prop("checked", true);
  }
  if ($("#id_tut-date_of_birth").val()) {
    $(".more_info__tutor").show();
    $("#id_is_tutor").prop("checked", true);
  }
  if ($("#id_is_tutor").is(":checked")) {
    $(".more_info__tutor").show();
  }
  if ($("#id_is_student").is(":checked")) {
    $(".more_info__student").show();
  }
});

/*
 * Setting the same dates of birth when entering student's birthday
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
      if ($("#id_is_tutor").is(":checked")) {
        $("#id_tut-date_of_birth").val($("#id_std-date_of_birth").val());
      }
    });
});

/*
 * Setting the same dates of birth when entering tutor's birthday
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
      if ($("#id_is_student").is(":checked")) {
        $("#id_std-date_of_birth").val($("#id_tut-date_of_birth").val());
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

/*
 * Display / hide additional information about student and tuter after
 * getting back to page
 */
if ($("#id_is_tutor").is(":checked")) {
  $(".more_info__tutor").show();
}
if ($("#id_is_student").is(":checked")) {
  $(".more_info__student").show();
}
if ($("#id_std-date_of_birth").val()) {
  $(".more_info__student").show();
  $("#id_is_student").prop("checked", true);
}
if ($("#id_tut-date_of_birth").val()) {
  $(".more_info__tutor").show();
  $("#id_is_tutor").prop("checked", true);
}
