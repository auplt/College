$(document).ready(function () {
  let studentInfo = $(".register_user__student");
  studentInfo.hide();
  let items = $("form p").length - 2;
  $("#id_is_student").parent().after(studentInfo);
  $("#id_is_student")[0].addEventListener("change", (event) => {
    if (event.target.checked) {
      studentInfo.show();
    } else {
      studentInfo.hide();
    }
  });
});

$(document).ready(function () {
  let tutorInfo = $(".register_user__tutor");
  tutorInfo.hide();
  let items = $("form p").length;
  $("#id_is_tutor").parent().after(tutorInfo);
  $("#id_is_tutor")[0].addEventListener("change", (event) => {
    if (event.target.checked) {
      tutorInfo.show();
    } else {
      tutorInfo.hide();
    }
  });
});

$(document).ready(function () {
  $("#id_std-date_of_birth")
    .datepicker({
      dateFormat: "dd.mm.yy",
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2024",
    })
    .on("input change", (event) => {
      $("#id_tut-date_of_birth").val($("#id_std-date_of_birth").val());
    });
});

$(document).ready(function () {
  $("#id_tut-date_of_birth")
    .datepicker({
      dateFormat: "dd.mm.yy",
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2024",
    })
    .on("input change", (event) => {
      $("#id_std-date_of_birth").val($("#id_tut-date_of_birth").val());
    });
});

$(document).ready(function () {
  $(".datepicker").datepicker({
    dateFormat: "dd.mm.yy",
    changeMonth: true,
    changeYear: true,
    yearRange: "1900:2024",
  });
});
