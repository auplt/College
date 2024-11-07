// JS Scripts specially for curriculum lesson group details template

/* Makes element width the same
 * For class curriculum_discipline_tutor_item_txt
 */
$(document).ready(function () {
  min_width = 0;
  $(".curriculum_discipline_tutor_item_general").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });
  if (min_width > 300) {
    min_width = 300;
  }
  $(".curriculum_discipline_tutor_item_general").css("width", min_width + "px");
});

/* Makes element width the same
 * For class curriculum_discipline
 */
$(document).ready(function () {
  min_width = 0;
  $(".curriculum_discipline").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });
  if (min_width > 300) {
    min_width = 300;
  }
  $(".curriculum_discipline").css("width", min_width + "px");
});

/* Makes element width the same
 * For class semester_number_controller_name
 */
$(document).ready(function () {
  min_width = 0;
  $(".item_semester_number_info_name").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });
  if (min_width > 300) {
    min_width = 300;
  }
  $(".item_semester_number_info_name").css("width", min_width + "px");
});

/* Collapse all list items except the first one */
$(document).ready(function () {
  $(".semester_number_controller")
    .slice(1, $(".semester_number_controller").length)
    .each(function () {
      let toggleNameCount = $(this)
        .parent()
        .nextUntil(".item_semester_number")
        .filter(".toggle_name").length;

      let toggleCtrlCount = $(this)
        .parent()
        .nextUntil(".item_semester_number")
        .filter(".toggle_ctrl").length;

      let toggleAdditionalCount = $(this)
        .parent()
        .nextUntil(".item_semester_number")
        .filter(".toggle_additional").length;

      let toggleDetailCount = $(this)
        .parent()
        .nextUntil(".item_semester_number")
        .filter(".toggle_detail").length;

      // Hidding found elements (group name)
      if (toggleNameCount) {
        $(this)
          .parent()
          .nextAll(".toggle_name")
          .slice(0, toggleNameCount)
          .slideToggle({ duration: 0 });
      }

      // Hidding found elements (delete button)
      if (toggleCtrlCount) {
        $(this)
          .parent()
          .nextAll(".toggle_ctrl")
          .slice(0, toggleCtrlCount)
          .slideToggle({ duration: 0 });
      }

      if (toggleAdditionalCount) {
        $(this)
          .parent()
          .nextAll(".toggle_additional")
          .slice(0, toggleAdditionalCount)
          .slideToggle({ duration: 0 });
      }
      if (toggleDetailCount) {
        $(this)
          .parent()
          .nextAll(".toggle_detail")
          .slice(0, toggleDetailCount)
          .slideToggle({ duration: 0 });
      }
    });
});
