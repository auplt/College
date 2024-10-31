/* Makes element width the same
 * For class curriculum_discipline_tutor_item_txt
 */
$(document).ready(function () {
  min_width = 0;
  $(".tt_lesson_info_time").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });
  if (min_width > 300) {
    min_width = 300;
  }
  $(".tt_lesson_info_time").css("width", min_width + "px");
});

/* Makes element width the same
 * For class curriculum_discipline_tutor_item_txt
 */
$(document).ready(function () {
  min_width = 0;
  $(".tt_lesson_info_discipline").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });
  if (min_width > 300) {
    min_width = 300;
  }
  $(".tt_lesson_info_discipline").css("width", min_width + "px");
});

/* Makes element width the same
 * For class curriculum_discipline_tutor_item_txt
 */
$(document).ready(function () {
  min_width = 0;
  $(".tt_lesson_classroom_name").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });
  if (min_width > 300) {
    min_width = 300;
  }
  $(".tt_lesson_classroom_name").css("width", min_width + "px");
});

/* Makes element width the same
 * For class curriculum_discipline_tutor_item_txt
 */
$(document).ready(function () {
  min_width = 0;
  $(".group_item_name").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });
  $(".tutor_item_name").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });

  if (min_width > 300) {
    min_width = 300;
  }

  $(".group_item_name").css("width", min_width + "px");
  $(".tutor_item_name").css("width", min_width + "px");
});
