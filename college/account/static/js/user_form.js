/*
 * Отображение / скрытие блока доп. информации о студенте
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
 * Отображение / скрытие блока доп. информации о преподавателе
 */
$(document).ready(function () {
  let tutorInfo = $(".more_info__tutor");
  tutorInfo.hide();
  let items = $("form p").length;
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

/*
 * Отображение / скрытие блока доп. информации при возврате на страницу в
 * случае ошибок в форме
 */
$(document).ready(function () {
  if ($("#id_std-date_of_birth").val()) {
    console.log("11");
    $(".more_info__student").show();
    $("#id_is_student").prop("checked", true);
  }
  if ($("#id_tut-date_of_birth").val()) {
    console.log("12");
    $(".more_info__tutor").show();
    $("#id_is_tutor").prop("checked", true);
  }
  if ($("#id_is_tutor").is(":checked")) {
    console.log("13");
    $(".more_info__tutor").show();
  }
  if ($("#id_is_student").is(":checked")) {
    console.log("14");
    $(".more_info__student").show();
  }
});

/*
 * Установление одинаковых дат рожения при внесении информации о
 * дате рождения студента
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
      console.log($("#id_is_tutor").val());
      if ($("#id_is_tutor").is(":checked")) {
        $("#id_tut-date_of_birth").val($("#id_std-date_of_birth").val());
      }
    });
});

/*
 * Установление одинаковых дат рожения при внесении информации о
 * дате рождения преподавателя
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
 * Добавление календаря при перезагрузке страницы
 */
$(document).ready(function () {
  $(".datepicker").datepicker({
    dateFormat: "dd.mm.yy",
    changeMonth: true,
    changeYear: true,
    yearRange: "1900:2024",
  });
});

console.log($("#id_is_tutor").val());
/*
 * Отображение / скрытие блока доп. информации о студенте и преподавателе
 * при возврате на страницу
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
  console.log("1");
  $(".more_info__tutor").show();
  $("#id_is_tutor").prop("checked", true);
}
