$(document).ready(function () {
  let studentInfo = $(".register_user__student");
  studentInfo.hide();
  let items = $("form p").length - 2;
  $("#id_is_student").parent().after(studentInfo);
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

$(document).ready(function () {
  let tutorInfo = $(".register_user__tutor");
  tutorInfo.hide();
  let items = $("form p").length;
  $("#id_is_tutor").parent().after(tutorInfo);
  $("#id_is_tutor")[0].addEventListener("change", (event) => {
    if (event.target.checked) {
      console.log("2");
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

$(document).ready(function () {
  if ($("#id_std-date_of_birth").val()) {
    console.log("11");
    $(".register_user__student").show();
    $("#id_is_student").prop("checked", true);
  }
  if ($("#id_tut-date_of_birth").val()) {
    console.log("12");
    $(".register_user__tutor").show();
    $("#id_is_tutor").prop("checked", true);
  }
  if ($("#id_is_tutor").is(":checked")) {
    console.log("13");
    $(".register_user__tutor").show();
  }
  if ($("#id_is_student").is(":checked")) {
    console.log("14");
    $(".register_user__student").show();
  }
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
      console.log($("#id_is_tutor").val());
      if ($("#id_is_tutor").is(":checked")) {
        $("#id_tut-date_of_birth").val($("#id_std-date_of_birth").val());
      }
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
      if ($("#id_is_student").is(":checked")) {
        $("#id_std-date_of_birth").val($("#id_tut-date_of_birth").val());
      }
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

console.log($("#id_is_tutor").val());
if ($("#id_is_tutor").is(":checked")) {
  $(".register_user__tutor").show();
}
if ($("#id_is_student").is(":checked")) {
  $(".register_user__student").show();
}
if ($("#id_std-date_of_birth").val()) {
  $(".register_user__student").show();
  $("#id_is_student").prop("checked", true);
}
if ($("#id_tut-date_of_birth").val()) {
  console.log("1");
  $(".register_user__tutor").show();
  $("#id_is_tutor").prop("checked", true);
}
